import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivate, IsPrivate_call
from keyboards.inline import kb_close_the_app, kb_start_question, kb_regisration_user, kb_menu_applications
from keyboards.inline.start_question import kb_cancel_all
from state import send_app_from_user, answer_from_admins
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asyncio import sleep
from loader import dp, bot
from data.config import cfg
from utils.db_api import register_commands as commands, applications_commands, admins_commands

devid = cfg['dev_id']
tehchatid = cfg['teh_chat_id']


# ХЕНДЛЕР НАЧАЛА ПОДАЧИ ЗАЯВКИ В ГРУППУ ТП
@dp.callback_query_handler(IsPrivate_call(), text_contains='start_question')
async def send_answer(call: types.CallbackQuery):
    await call.message.delete()
    global msg_answer
    try:
        user = await commands.select_user(call.from_user.id)
        markup_4 = InlineKeyboardMarkup(row_width=1,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='❌Отмена подачи заявки❌',
                                                                     callback_data='quit')
                                            ]
                                        ])
        if user.status == 'active':
            await call.answer(cache_time=5)

            msg_answer = await call.message.answer(
                f"📝 Здравствуйте, формат заявки: Вы указываете магазин и номер кассы, "
                f"ваша проблема с которой вы столкнулись (Можно и нужно прикрепить фото):", reply_markup=markup_4)

            await send_app_from_user.text.set()
        elif user.status == 'baned':
            await call.message.answer('⛔Вы забанены!⛔')
    except Exception:
        await call.message.answer(
            f'Приветствую тебя @<a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a>!\n'
            f'Вы попали в <b>тех.поддержку</b> 🛠\n'
            f'Для продолжения вам нужно <b>зарегистрироваться</b>, '
            'нажмите кнопку 📝<b>Регистрация</b> или воспользуйтесь командой <b>/reg</b>',
            reply_markup=kb_regisration_user)


@dp.message_handler(IsPrivate(), state=send_app_from_user)
async def notice_text(message: types.Message, state: FSMContext):
    await message.delete()
    answer = message.text
    await state.update_data(text=answer)
    await message.answer(text=f'<b>Вы написали</b>: {answer}', reply_markup=kb_menu_applications)
    await send_app_from_user.state.set()
    await asyncio.sleep(3)
    await msg_answer.delete()


# Отправка сообщений в группу ТП с текстом
@dp.callback_query_handler(text='next', state=send_app_from_user.state)
async def start_notice(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer(cache_time=5)
    markupdelete = types.ReplyKeyboardRemove()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()

    # Запись в БД заявки от пользователя
    users = await commands.select_user(call.from_user.id)
    app_id = await applications_commands.count_id_application() + 1
    await applications_commands.add_application(app_id=app_id,
                                                user_id=call.from_user.id,
                                                tg_first_name=call.from_user.first_name,
                                                tg_last_name=call.from_user.last_name,
                                                famils=users.famils,
                                                username=users.username,
                                                phone=users.phone,
                                                magazin=users.magazin,
                                                text_app=text,
                                                reply_text_admin='NULL',
                                                by_admin=0)

    # Кнопка Ответить от сотрудника технической поддержки когда присылают текст
    news_callback = CallbackData("reply_answer", "user_id", "app_id")
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_reply = InlineKeyboardButton(text='💬 Ответить',
                                     callback_data=news_callback.new(user_id=call.message.chat.id, app_id=app_id))
    keyboard.add(btn_reply)
    try:
        await dp.bot.send_message(tehchatid, text=f"✉ | Новый вопрос\n"
                                                  f"<b>#️⃣Номер заявки: {app_id}</b>\n"
                                                  f"<b>❗Статус заявки:</b> 🚫Открыта!\n"
                                                  f'<b>👤От: <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a></b>\n'
                                                  f"<b>🆔ID:</b> {call.from_user.id}\n"
                                                  f"<b>👤Фамилия:</b> {users.famils} \n"
                                                  f"<b>👤Имя:</b> {users.username} \n"
                                                  f"<b>📞Номер телефона:</b> {users.phone}  \n"
                                                  f"<b>🏢Организация:</b> {users.magazin} \n"
                                                  f"<b>⁉Вопрос:</b> <code>{text}</code>\n\n📝 Чтобы ответить на "
                                                  f"вопрос нажмите кнопку <b>💬Ответить</b>",
                                  reply_markup=keyboard)
        await sleep(0.33)
    except Exception as e:
        cid = call.message.chat.id
        await call.message.answer(
            f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await dp.bot.send_message(devid,
                                  f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")
    await call.message.answer('✉ Ваш вопрос был отослан! Ожидайте ответа от тех.поддержки.',
                              reply_markup=markupdelete)


@dp.callback_query_handler(text='add_photo', state=send_app_from_user.state)
async def add_photo(call: types.CallbackQuery):
    await call.message.delete()
    global msg_photo_answer
    msg_photo_answer = await call.message.answer('<b>Пришлите фото</b>:', reply_markup=kb_cancel_all)
    await send_app_from_user.photo.set()


@dp.message_handler(IsPrivate(), state=send_app_from_user.photo, content_types=types.ContentType.PHOTO)
async def send_text(message: types.Message, state: FSMContext):
    await msg_photo_answer.delete()
    await message.delete()
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup_2 = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='⬆Отправить', callback_data='next'),
                                            InlineKeyboardButton(text='❌Отменить', callback_data='quit')
                                        ]
                                    ])
    await message.answer_photo(photo=photo, caption=f'<b>Вы написали</b>: {text}\n'
                                                    f'И прикрепили фото, теперь нажмите кнопку ⬆Отправить',
                               reply_markup=markup_2)


# Отправка сообщений в группу ТП с фото
@dp.callback_query_handler(text='next', state=send_app_from_user.photo)
async def get_start_notice(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer(cache_time=5)
    markupdelete = types.ReplyKeyboardRemove()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()

    # ----------------------------------БЛОК ОТВЕТА ПОЛЬЗОВАТЕЛЮ----------------------------------------------------
    # Запись в БД заявки от пользователя
    users = await commands.select_user(call.from_user.id)
    app_id = await applications_commands.count_id_application() + 1
    await applications_commands.add_application(app_id=app_id,
                                                user_id=call.from_user.id,
                                                tg_first_name=call.from_user.first_name,
                                                tg_last_name=call.from_user.last_name,
                                                famils=users.famils,
                                                username=users.username,
                                                phone=users.phone,
                                                magazin=users.magazin,
                                                text_app=text,
                                                reply_text_admin='NULL',
                                                by_admin=0)

    # Кнопка Ответить от сотрудника технической поддержки когда присылают фото
    news_callback = CallbackData("reply_answer", "user_id", "app_id")
    keyboard = InlineKeyboardMarkup(row_width=1)
    menu_1 = InlineKeyboardButton(text='💬 Ответить',
                                  callback_data=news_callback.new(user_id=call.message.chat.id, app_id=app_id))
    keyboard.add(menu_1)

    # Отправка заявки с фото в группу ТП
    try:
        await dp.bot.send_photo(tehchatid, photo=photo, caption=f"✉ | Новый вопрос\n"
                                                                f"<b>#️⃣Номер заявки: {app_id}</b>\n"
                                                                f"<b>❗Статус заявки:</b> 🚫Открыта!\n"
                                                                f'<b>👤От: <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a></b>\n'
                                                                f'<b>🆔ID:</b> {call.from_user.id}\n'
                                                                f"<b>👤Фамилия:</b> {users.famils} \n"
                                                                f"<b>👤Имя:</b> {users.username} \n"
                                                                f"<b>📞Номер телефона:</b> {users.phone}  \n"
                                                                f"<b>🏢Организация:</b> {users.magazin} \n"
                                                                f"<b>⁉Вопрос:</b> <code>{text}</code>\n\n📝 Чтобы "
                                                                f"ответить на вопрос нажмите кнопку <b>💬Ответить</b>",
                                reply_markup=keyboard)
        await sleep(0.33)
    except Exception as e:
        await call.message.answer(
            f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await dp.bot.send_message(devid,
                                  f"Случилась <b>ошибка</b> в чате <b>{call.message.chat.id}</b>\nСтатус ошибки: <code>{e}</code>")
    await call.message.answer('✉ Ваш вопрос и фото были отосланы! Ожидайте ответа от тех.поддержки.',
                              reply_markup=markupdelete)


@dp.message_handler(IsPrivate(), state=send_app_from_user.photo)
async def no_photo(message: types.Message):
    markup_3 = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='❌Отменить', callback_data='quit')
                                        ]
                                    ])
    await message.answer('Пришли мне фото', reply_markup=markup_3)


@dp.callback_query_handler(text='quit',
                           state=[send_app_from_user.text, send_app_from_user.photo, send_app_from_user.state])
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.delete()
    await call.message.answer('⛔️Вы отменили подачу заявки\n'
                              'и можете начать сначала нажав кнопку ✉ <b>Задать вопрос</b>',
                              reply_markup=kb_start_question)
    user = await commands.select_user(call.from_user.id)
    await bot.send_message(tehchatid,
                           f'❌ Пользователь <b>{user.famils} {user.username}</b> из Организации <b>{user.magazin}</b> '
                           f'отменил подачу заявки!')


# -----------------------------------------БЛОК ОТВЕТА НА ЗАЯВКУ С ФОТО И БЕЗ ФОТО--------------------------------------
@dp.callback_query_handler(text_contains='reply_answer')
async def reply_answer_yes(call: types.CallbackQuery, state: FSMContext):
    message_id = call.message.message_id
    admin_id = call.from_user.id
    await call.answer(cache_time=5)
    callback_data = call.data.split(":")
    user_id = callback_data[1]
    app_id = int(callback_data[2])
    answer = call.message.text
    user = await commands.select_user_id(int(user_id))
    reply_message_from_admin = await dp.bot.send_message(chat_id=tehchatid,
                                                         text=f"Введите ваш ответ для <b>{user.famils} {user.username}</b>:",
                                                         reply_to_message_id=answer)
    await state.update_data(user_id=user_id, app_id=app_id, message_id=message_id,
                            reply_message_from_admin=reply_message_from_admin)

    # Меняем кнопку Ответить до ответа
    kb_send_answer = InlineKeyboardMarkup(row=1)
    admin = await admins_commands.select_admin(int(admin_id))
    menu = InlineKeyboardButton(text=f'📝Заявку взял {admin.first_name}', callback_data="answer")
    kb_send_answer.add(menu)
    await dp.bot.edit_message_reply_markup(chat_id=tehchatid, message_id=message_id, reply_markup=kb_send_answer)
    await answer_from_admins.text.set()


@dp.message_handler(state=answer_from_admins.text, content_types=types.ContentType.ANY)
async def mailing_text(message: types.Message, state: FSMContext):
    global message_ids
    global app_id
    data = await state.get_data()
    user_id = data.get('user_id')
    app_id = data.get('app_id')
    reply_message_from_admin = data.get('reply_message_from_admin')
    message_ids = data.get('message_id')

    # Обрабатываем ситуацию, если сообщение - это фото
    if message.content_type == "photo":
        # Получаем текст и отправляем его вместе с фото
        text = message.caption if message.caption else "Фото без текста"
        # Получаем ID ФОТО
        photo_file_id = message.photo[-1].file_id
        # Отправляем сообщение в чат пользователю
        await dp.bot.send_photo(chat_id=user_id, reply_to_message_id=reply_message_from_admin, photo=photo_file_id,
                                caption=f"💬 Новое уведомление!\nОтвет от тех.поддержки:\n\n<b>{text}</b>")

        await message.reply('✅ Вы успешно ответили на вопрос!')
        await bot.send_message(user_id, f"⚠️Просьба <b>закрывать заявки</b> после ответа от Технической поддержки⚠️")
        await bot.send_message(user_id, f"Заявка закрыта ❓❓❓", reply_markup=kb_close_the_app)

    else:  # Обрабатываем другие типы сообщений
        text = message.text
        await dp.bot.send_message(chat_id=user_id, reply_to_message_id=reply_message_from_admin,
                                  text=f"💬 Новое уведомление!\nОтвет от тех.поддержки:\n\n<b>{text}</b>")

        # Меняем кнопку Ответить после того как ответили на заявку
        kb_send_answer = InlineKeyboardMarkup(row=1)
        menu = InlineKeyboardButton(text='✅Ответ отправлен', callback_data="answer")
        kb_send_answer.add(menu)
        await dp.bot.edit_message_reply_markup(chat_id=tehchatid, message_id=message_ids,
                                               reply_markup=kb_send_answer)

        await message.reply('✅ Вы успешно ответили на вопрос!')
        await bot.send_message(user_id, f"⚠️Просьба <b>закрывать заявки</b> после ответа от Технической поддержки⚠️")
        await bot.send_message(user_id, f"Заявка закрыта ❓❓❓", reply_markup=kb_close_the_app)

    # Запись в БД ответа от сотрудника ТП(Администратора)
    await applications_commands.answer_edit_reply(app_id=app_id,
                                                  reply_text_admin=text,
                                                  by_admin=message.from_user.id)
    await state.finish()


# ЗАКРЫТИЕ ЗАЯВКИ ОТ ПОЛЬЗОВАТЕЛЯ ЧЕРЕЗ ИНЛАИН КНОПКУ "Заявка закрыта"
@dp.callback_query_handler(IsPrivate_call(), text_contains='app_closed')
async def app_closed(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    reply_msg = await call.message.reply(f'Вы успешно <b>закрыли</b> заявку. 👍')
    await call.message.answer(f'Чтобы задать вопрос сначала,\n'
                              f'нажмите кнопку <b>✉ Задать вопрос</b>', reply_markup=kb_start_question)
    user = await commands.select_user(call.from_user.id)
    await bot.send_message(tehchatid,
                           f'✅ Заявка №{app_id} от <b>{user.famils} {user.username}</b> из Организации <b>{user.magazin}</b> '
                           f'успешно закрыта!')

    # Меняем кнопку Ответить после закрытия заявка
    kb_send_answer = InlineKeyboardMarkup(row=1)
    menu = InlineKeyboardButton(text=f'✅ Заявка закрыта!', callback_data="answer")
    kb_send_answer.add(menu)

    # message_id из хендлера ответа на заявку
    await dp.bot.edit_message_reply_markup(chat_id=tehchatid, message_id=message_ids,

                                           reply_markup=kb_send_answer)
    await state.finish()
    await asyncio.sleep(5)
    await call.message.delete()
    await reply_msg.delete()


# НЕ ЗАКРЫТИЕ ЗАЯВКИ ОТ ПОЛЬЗОВАТЕЛЯ ЧЕРЕЗ ИНЛАИН КНОПКУ "Заявка не закрыта"
@dp.callback_query_handler(text_contains='app_open')
async def app_open(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    await state.finish()
    await call.message.answer('Продолжите диалог с тех.поддержкой: ')
    await send_app_from_user.text.set()
    user = await commands.select_user(call.from_user.id)
    await bot.send_message(tehchatid,
                           f'💬Пользователь <b>{user.famils} {user.username}</b> из Организации <b>{user.magazin}</b> '
                           f'не закрыл заявку, и продолжил диалог!')

    # Меняем кнопку Ответить после закрытия заявка
    kb_send_answer = InlineKeyboardMarkup(row=1)
    menu = InlineKeyboardButton(text=f'❌ Заявка не закрыта!', callback_data="answer")
    kb_send_answer.add(menu)

    # message_id из колбэка ответа на заявку
    await dp.bot.edit_message_reply_markup(chat_id=tehchatid, message_id=message_ids,

                                           reply_markup=kb_send_answer)
