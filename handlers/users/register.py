import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import IsPrivate, IsPrivate_call
# from keyboards.default import kb_menu_magazinreply
from keyboards.inline import kb_regisration_user, kb_cancel_registration_users, kb_start_question, kb_menu_magazinreply
from loader import dp, bot
from data.config import cfg
from state import reg
from utils.db_api import register_commands
from utils.misc import rate_limit
import re

teh_chat_id = cfg['teh_chat_id']


# Хендлер отмены состояния регистрации
@dp.callback_query_handler(IsPrivate_call(), text_contains='cancel_registration_users', state=[reg.familiya, reg.name, reg.phone, reg.magazine])
async def quit_registration(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    await state.finish()
    await call.message.answer('❎ <b>Регистрация отменена</b> ❎\n\n'
                              'Вы отменили регистрацию и можете пройти\n'
                              'повторно нажав клавишу 📝 <b>Регистрация</b>', reply_markup=kb_regisration_user)


# Хендлер регистрации пользователей через инлаин кнопку
@rate_limit(limit=5)
@dp.callback_query_handler(IsPrivate_call(), text_contains='registration_users')
async def registration_user(call: types.CallbackQuery):
    global msg_start_reg
    await call.answer(cache_time=5)
    await call.message.delete()
    msg_start_reg = await call.message.answer('Приветствую тебя! началась регистрация,\nВведите свою Фамилию:\n'
                         'Например: Иванов', disable_web_page_preview=True, reply_markup=kb_cancel_registration_users)
    await reg.familiya.set()


# Хендлер регистрации пользователей через команду /reg
@rate_limit(limit=5)
@dp.message_handler(IsPrivate(), commands=['reg'])
async def registration_user_command(message: types.Message):
    await message.answer('Приветствую тебя! началась регистрация,\nВведите свою Фамилию:\n'
                         'Например: Иванов', disable_web_page_preview=True, reply_markup=kb_cancel_registration_users)
    await reg.familiya.set()


# Хендлер состояния Фамилии
@dp.message_handler(state=reg.familiya)
async def familiya_user(message: types.Message, state: FSMContext):
    global msg_name
    global message_id_familiya
    global message_chat_familiya
    text_familiya = message.text
    message_chat_familiya = message.chat.id
    message_id_familiya = message.message_id

    await state.update_data(familiya=text_familiya)
    msg_name = await message.answer('Введите своё Имя:\n'
                         'Например: Иван ')
    await reg.name.set()


# Хендлер состояния Имя
@dp.message_handler(state=reg.name)
async def name_user(message: types.Message, state: FSMContext):
    global msg_number
    global message_id_nameuser
    global message_chat_nameuser
    text_name = message.text
    message_chat_nameuser = message.chat.id
    message_id_nameuser = message.message_id

    await state.update_data(name=text_name)
    msg_number = await message.answer(f'Введите свой номер телефона с +7:\n'
                                      f'Например: +7ХХХХХХХХХХ')
    await reg.phone.set()


# Хендлер состояния Номера Телефона
@dp.message_handler(state=reg.phone)
async def phone_user(message: types.Message, state: FSMContext):
    global msg_mag
    global message_chat_phoneuser
    global message_id_phoneuser
    answer = message.text
    message_chat_phoneuser = message.chat.id
    message_id_phoneuser = message.message_id
    pattern = r'(^\+7)((\d{10})|(\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}))'
    try:
        if re.match(pattern, answer):
                await state.update_data(phone=answer)
                msg_mag = await message.answer('Выберите название своей организации или магазина:\n'
                                 'Например: МояКомпания', reply_markup=kb_menu_magazinreply)
                await reg.magazine.set()
        else:
            await message.answer('Введите корректный номер телефона, номер должен начинаться с +7:')
    except Exception:
        await message.answer('Введите корректный номер телефона, номер телефона введен не правильно!')


# Хендлер состояния Регистрации Организации / Магазина
@dp.callback_query_handler(IsPrivate_call(), text_contains="mag_", state=reg.magazine)
async def magazine_user(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    global msg_actual
    who = "@" + call.from_user.get_mention(as_html=True)
    # берет клавиатуру и срезает приставку mag_ далее из словаря вытаскивает названия на русском
    magazin = call.data[4:]
    # словарь Организаций на русском без приставки mag_
    magazins = {'test1': "Магазин Тест 1",
                'test2': "Магазин Тест 2",
                'test3': "Магазин Тест 3",
                'test4': "Магазин Тест 4",
                'test5': "Магазин Тест 5",
                'test6': "Магазин Тест 6",
                'test7': "Магазин Тест 7",
                'test8': "Магазин Тест 8",
                'test9': "Магазин Тест 9",
                'test10': "Магазин Тест 10",
                'test11': "Магазин Тест 11"}

    actual_magazin = magazins[magazin]

    # Удаление сообщений после успешной регистрации
    msg_actual = await call.message.answer(f"Вы выбрали <b>{actual_magazin}</b>")

    await state.update_data(magazine=actual_magazin)
    data = await state.get_data()
    familname = data.get('familiya')
    usernames = data.get('name')
    phone = data.get('phone')
    magaz = data.get('magazine')
    await register_commands.new_registration(user_id=call.from_user.id,
                                             tg_first_name=call.from_user.first_name,
                                             tg_last_name=call.from_user.last_name,
                                             famils=familname.capitalize(),
                                             username=usernames.capitalize(),
                                             phone=phone,
                                             magazin=magaz,
                                             status='active',
                                             access=int('0'),
                                             reason='no reason')


    await call.message.answer(f'✅<b>Регистрация успешно завершена!</b>\n'
                              f'<b>Ваши данные</b>:\n'
                              f'<b>Фамилия</b>: {familname}\n'
                              f'<b>Имя:</b> {usernames}\n'
                              f'<b>Телефон</b>: {phone}\n'
                              f'<b>Магазин</b>: {magaz}\n'
                              f'Теперь вы можете задать вопрос\n'
                              f'Нажав кнопку ✉ <b>Задать вопрос</b>\n', reply_markup=kb_start_question)


    await bot.send_message(teh_chat_id, f'📌<b>У нас новый пользователь</b>\n'
                         f'<b>📍NickName</b>: {who}\n'
                         f'<b>🆔ID:</b> {call.from_user.id}\n'
                         f'<b>👤Фамилия</b>: {familname}\n'
                         f'<b>👤Имя</b>: {usernames}\n'
                         f'<b>📞Телефон</b>: {phone}\n'
                         f'<b>🏢Магазин</b>: {magaz}\n')
    await state.finish()

    # Удаление всех сообщений после завершения регистрации у пользователя через 1 секунду
    await asyncio.sleep(1)
    await msg_start_reg.delete()
    await msg_mag.delete()
    await bot.delete_message(message_chat_familiya, message_id_familiya)
    await bot.delete_message(message_chat_nameuser, message_id_nameuser)
    await bot.delete_message(message_chat_phoneuser, message_id_phoneuser)
    await msg_name.delete()
    await msg_number.delete()
    await msg_actual.delete()