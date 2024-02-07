from asyncio import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api import register_commands as commands
from utils.db_api import admins_commands as b_commands
from state import send_notice_alladmins
from loader import dp
from filters import IsPrivate, IsAdminCheck, IsPrivate_call
from data.config import cfg

devid = cfg['dev_id']


# ---------------------------------БЛОК ОТПРАВКИ УВЕДОМЛЕНИЯ ВСЕМ СОТРУДНИКАМ ТП----------------------------------------
@dp.callback_query_handler(IsPrivate_call(), IsAdminCheck(), text="notice_all_admins")
async def get_send_notice_admins(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    markup_4 = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Отменить', callback_data='quit')
                                        ]
                                    ])
    await call.message.answer(f'✏Введите текст для отправки уведомления тех.поддержке:', reply_markup=markup_4)
    await send_notice_alladmins.text.set()


@dp.message_handler(IsPrivate(), state=send_notice_alladmins)
async def notice_text(message: types.Message, state: FSMContext):
    answer = message.text
    markup_1 = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo'),
                                            InlineKeyboardButton(text='Отправить', callback_data='next'),
                                            InlineKeyboardButton(text='Отменить', callback_data='quit')
                                        ]
                                    ])
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=markup_1)
    await send_notice_alladmins.state.set()


@dp.callback_query_handler(text='next', state=send_notice_alladmins.state)
async def start_notice(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user.user_id,
                                      text=f"✉ | ❗️❗️❗️Новое уведомление для Тех Поддержки❗️❗️❗️\n"
                                           f"Текст: ⚠️<b>{text}</b>⚠️\n")
            await sleep(0.33)
        except Exception as e:
            cid = user.user_id
            await call.message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
            await dp.bot.send_message(devid,
                                      f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")
    await call.message.answer('✉ Ваше уведомление для всех пользователей было отослано.')


@dp.callback_query_handler(text='add_photo', state=send_notice_alladmins.state)
async def add_photo(call: types.CallbackQuery):
    await call.message.answer('Пришлите фото')
    await send_notice_alladmins.photo.set()


@dp.message_handler(IsPrivate(), state=send_notice_alladmins.photo, content_types=types.ContentType.PHOTO)
async def send_text(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup_2 = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Отправить', callback_data='next'),
                                            InlineKeyboardButton(text='Отменить', callback_data='quit')
                                        ]
                                    ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup_2)


@dp.callback_query_handler(text='next', state=send_notice_alladmins.photo)
async def get_start_notice(call: types.CallbackQuery, state: FSMContext):
    admins = await b_commands.select_all_admins()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()
    for admin in admins:
        try:
            await dp.bot.send_photo(chat_id=admin.user_id, photo=photo,
                                    caption=f"✉ | ❗️❗️❗️Новое уведомление от Тех Поддержки❗️❗️❗️\n"
                                            f"Текст: ⚠️<b>{text}</b>⚠️\n")
            await sleep(0.33)
        except Exception as e:
            cid = admin.user_id
            await call.message.answer(
                f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
            await dp.bot.send_message(devid,
                                      f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")
    await call.message.answer('✉ Ваше уведомление для всех пользователей было отослано.')


@dp.message_handler(IsPrivate(), state=send_notice_alladmins.photo)
async def no_photo(message: types.Message):
    markup_3 = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Отменить', callback_data='quit')
                                        ]
                                    ])
    await message.answer('Пришли мне фото', reply_markup=markup_3)


@dp.callback_query_handler(text='quit',
                           state=[send_notice_alladmins.text, send_notice_alladmins.photo, send_notice_alladmins.state])
async def quit(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer('❌Уведомление отменено')
# ---------------------------------КОНЕЦ БЛОКА ОТПРАВКИ УВЕДОМЛЕНИЯ ВСЕМ СОТРУДНИКАМ ТП---------------------------------
