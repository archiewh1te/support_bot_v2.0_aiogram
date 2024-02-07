from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api import register_commands as commands
from loader import dp
from filters import IsAdminCheck, IsPrivate_call

# --------------------------------------БЛОК ПРОСМОТРА ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ---------------------------------------------

# CallbackData для функции просмотра профиля пользователя
profile_callback = CallbackData("user_profile", "user_id")

# Определяем количество пользователей на одной странице
USERS_PER_PAGE = 5


@dp.callback_query_handler(IsAdminCheck(), IsPrivate_call(), text='check_user_profile')
async def get_all_users(call: types.CallbackQuery):
    await call.answer()
    # Получаем список пользователей
    users = await commands.select_all_users()
    page_number = 1  # изначально отображаем первую страницу пользователей
    await show_users_page(call, users, page_number)


# Отображение списка пользователей на странице с заданным номером
async def show_users_page(call, users, page_number):
    start_index = (page_number - 1) * USERS_PER_PAGE
    end_index = start_index + USERS_PER_PAGE
    users_for_page = users[start_index:end_index]

    # Создание клавиатуры страницы
    kb_check_all_users = InlineKeyboardMarkup(row_width=3)
    for user in users_for_page:
        famils = user.famils.replace('(', ' ')
        username = user.username.replace('(', ' ')
        btn_profile = InlineKeyboardButton(text=f'👤{famils} {username}',
                                           callback_data=profile_callback.new(user_id=user.user_id))
        kb_check_all_users.add(btn_profile)

    # Создание кнопок пагинации
    total_pages = -(-len(users) // USERS_PER_PAGE)  # Округление количества страниц вверх
    page_buttons = generate_page_buttons(page_number, total_pages)
    kb_check_all_users.row(*page_buttons)

    btn_cancel = InlineKeyboardButton(text='⬅Назад ', callback_data='cancel')
    kb_check_all_users.add(btn_cancel)
    await call.message.edit_text('<b>Выберите пользователя:</b> ', reply_markup=kb_check_all_users)


# Генерация кнопок пагинации
def generate_page_buttons(page_number, total_pages):
    buttons = []
    if page_number > 1:
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prev_check_page_{page_number}"))
    buttons.append(InlineKeyboardButton(text=f'{page_number} / {total_pages}', callback_data='total_check'))
    if page_number < total_pages:
        buttons.append(InlineKeyboardButton(text="▶️ Вперед", callback_data=f"next_check_page_{page_number}"))
    return buttons


# Обработка нажатия на кнопку пагинации
@dp.callback_query_handler(lambda query: query.data.startswith(('prev_check', 'next_check')))
async def process_page_button(call: types.CallbackQuery):
    page_number = int(call.data.split('_')[-1])

    if call.data.startswith('prev_check'):
        page_number -= 1
    else:
        page_number += 1

    users = await commands.select_all_users()
    await show_users_page(call, users, page_number)


@dp.callback_query_handler(text_contains='user_profile')
async def get_user_profile(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data.split(":")
    user_id = callback_data[1]
    users = await commands.select_registration_by_user_id(int(user_id))
    kb_back_info = InlineKeyboardMarkup(row_width=1)
    btn_back_users = InlineKeyboardButton(text='⬅Назад ', callback_data='check_user_profile')
    kb_back_info.add(btn_back_users)
    await call.message.edit_text(text=f'🔎Информация о пользователе:\n'
                                      f'<b>🆔</b> - {users.user_id}\n'
                                      f'<b>👤Имя</b>: {users.username}\n'
                                      f'<b>👤Фамилия</b>: {users.famils}\n'
                                      f'<b>first_name</b>: {users.tg_first_name}\n'
                                      f'<b>last_name</b>: {users.tg_last_name}\n'
                                      f'<b>🕵️‍Статус</b>: {users.status}\n'
                                      f'<b>📞Телефон</b>: {users.phone}\n'
                                      f'<b>🏢Магазин</b>: {users.magazin}\n', reply_markup=kb_back_info)

# ---------------------------------КОНЕЦ БЛОКА ПРОСМОТРА ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ-------------------------------------------
