import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from state.edit_all_users import edit_famils_user
from utils.db_api import register_commands as commands
from utils.db_api import register_commands as a_commands
from loader import dp, bot
from filters import IsAdminCheck, IsPrivate_call

# -------------------------------------БЛОК РЕДАКТИРОВАНИЯ ФАМИЛИИ------------------------------------------------------

# CallbackData для функции редактирования фамилий пользователя
edit_famils_callback = CallbackData("edit_famils", "user_id")

# Определяем количество пользователей на одной странице
USERS_PER_PAGE = 5


@dp.callback_query_handler(IsAdminCheck(), IsPrivate_call(), text='edit_famils_users')
async def get_edit_famils_users(call: types.CallbackQuery):
    await call.answer()
    # Получаем список пользователей
    users = await commands.select_all_users()
    page_number = 1  # изначально отображаем первую страницу пользователей
    await show_users_page(call, users, page_number)


# Отображение списка пользователей на странице с заданным номером
async def show_users_page(call, users, page_number):
    global msg_users
    start_index = (page_number - 1) * USERS_PER_PAGE
    end_index = start_index + USERS_PER_PAGE
    users_for_page = users[start_index:end_index]

    # Создание клавиатуры страницы
    kb_edit_famils = InlineKeyboardMarkup(row_width=1)
    for user in users_for_page:
        famils = user.famils.replace('(', ' ')
        username = user.username.replace('(', ' ')
        edit_famils_callback = CallbackData("edit_famils", "user_id")
        btn_profile = InlineKeyboardButton(text=f'👤{famils} {username}',
                                           callback_data=edit_famils_callback.new(user_id=user.user_id))
        kb_edit_famils.add(btn_profile)

    # Создание кнопок пагинации
    total_pages = -(-len(users) // USERS_PER_PAGE)  # Округление количества страниц вверх
    page_buttons = generate_page_buttons(page_number, total_pages)
    kb_edit_famils.row(*page_buttons)

    btn_cancel = InlineKeyboardButton(text='⬅Назад', callback_data='cancel')
    kb_edit_famils.add(btn_cancel)

    msg_users = await call.message.edit_text(f'<b>Выберите пользователя:</b> ', reply_markup=kb_edit_famils)


# Генерация кнопок пагинации
def generate_page_buttons(page_number, total_pages):
    buttons = []
    if page_number > 1:
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prev_famils_page_{page_number}"))
    buttons.append(InlineKeyboardButton(text=f'{page_number} / {total_pages}', callback_data='total_user_famils'))
    if page_number < total_pages:
        buttons.append(InlineKeyboardButton(text="▶️ Вперед", callback_data=f"next_famils_page_{page_number}"))
    return buttons


# Обработка нажатия на кнопку пагинации
@dp.callback_query_handler(lambda query: query.data.startswith(('prev_famils', 'next_famils')))
async def process_page_button(call: types.CallbackQuery):
    page_number = int(call.data.split('_')[-1])

    if call.data.startswith('prev_famils'):
        page_number -= 1
    else:
        page_number += 1

    users = await commands.select_all_users()
    await show_users_page(call, users, page_number)


@dp.callback_query_handler(text_contains='edit_famils')
async def get_edit_famils(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    callback_data = call.data.split(":")
    print(callback_data)
    user_id = callback_data[1]
    users = await commands.select_registration_by_user_id(int(user_id))
    answer = call.message.text
    global edit_famils
    edit_famils = await dp.bot.send_message(chat_id=call.message.chat.id,
                                            text=f"Введите Фамилию для <b>{users.famils}</b> <b>{users.username}</b> :",
                                            reply_to_message_id=answer)
    await state.update_data(user_id=user_id, reply_message_from_admin=edit_famils)
    await edit_famils_user.text.set()


@dp.message_handler(state=edit_famils_user.text)
async def get_edit_text(message: types.Message, state: FSMContext):
    global msg_edit_famils
    global msg_chat_id, msg_id
    msg_chat_id = message.chat.id
    msg_id = message.message_id
    text = message.text
    data = await state.get_data()
    user_id = data.get('user_id')
    kb_back = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton(text='⬅Назад', callback_data='edit_famils_users')
    kb_back.add(btn_back)
    await a_commands.update_famils(user_id=int(user_id), famils=text)
    users = await commands.select_user_id(int(user_id))
    msg_edit_famils = await message.answer(
        f'✅ Вы успешно сменили <b>Фамилию</b> для пользователя <b>{users.famils}</b> <b>{users.username}</b> на <code>{text}</code>',
        reply_markup=kb_back)
    await state.finish()

    # Удаление сообщений после того как изменили Фамилию пользователю через 1 секунду
    await asyncio.sleep(1)
    await bot.delete_message(msg_chat_id, msg_id)
    await msg_users.delete()
    await edit_famils.delete()

# -------------------------------------КОНЕЦ БЛОКА РЕДАКТИРОВАНИЯ ФАМИЛИИ ПОЛЬЗОВАТЕЛЯ----------------------------------
