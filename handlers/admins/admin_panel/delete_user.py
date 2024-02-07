from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api import register_commands as commands
from utils.db_api import register_commands as a_commands
from loader import dp
from filters import IsAdminCheck, IsPrivate_call

# -----------------------------БЛОК УДАЛЕНИЯ ПОЛЬЗОВАТЕЛЯ ИЗ БД---------------------------------------------------------

# CallbackData для функции удаления пользователя
del_user_callback = CallbackData("delete_user", "user_id")

# Определяем количество пользователей на одной странице
USERS_PER_PAGE = 5


@dp.callback_query_handler(IsAdminCheck(), IsPrivate_call(), text='delete_users')
async def get_del_users(call: types.CallbackQuery):
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
    kb_check_all_users = InlineKeyboardMarkup(row_width=1)
    for user in users_for_page:
        famils = user.famils.replace('(', ' ')
        username = user.username.replace('(', ' ')
        del_user_callback = CallbackData("delete_user", "user_id")
        btn_profile = InlineKeyboardButton(text=f'👤{famils} {username} ',
                                           callback_data=del_user_callback.new(user_id=user.user_id))
        kb_check_all_users.add(btn_profile)

    # Создание кнопок пагинации
    total_pages = -(-len(users) // USERS_PER_PAGE)  # Округление количества страниц вверх
    page_buttons = generate_page_buttons(page_number, total_pages)
    kb_check_all_users.row(*page_buttons)

    btn_cancel = InlineKeyboardButton(text='⬅Назад ', callback_data='cancel')
    kb_check_all_users.add(btn_cancel)

    await call.message.edit_text('Выберите пользователя для <b>Удаления</b>:', reply_markup=kb_check_all_users)


# Генерация кнопок пагинации
def generate_page_buttons(page_number, total_pages):
    buttons = []
    if page_number > 1:
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prev_delete_page_{page_number}"))
    buttons.append(InlineKeyboardButton(text=f'{page_number} / {total_pages}', callback_data='total_user_delete'))
    if page_number < total_pages:
        buttons.append(InlineKeyboardButton(text="▶️ Вперед", callback_data=f"next_delete_page_{page_number}"))
    return buttons


# Обработка нажатия на кнопку пагинации
@dp.callback_query_handler(lambda query: query.data.startswith(('prev_delete', 'next_delete')))
async def process_page_button(call: types.CallbackQuery):
    page_number = int(call.data.split('_')[-1])

    if call.data.startswith('prev_delete'):
        page_number -= 1
    else:
        page_number += 1

    users = await commands.select_all_users()
    await show_users_page(call, users, page_number)


@dp.callback_query_handler(text_contains='delete_user')
async def delete_user(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    callback_data = call.data.split(":")
    user_id = callback_data[1]
    await a_commands.delete_user(user_id=int(user_id))
    await call.message.answer(f'✅ Вы успешно <b>Удалили</b> пользователя!')

# -------------------------------------КОНЕЦ БЛОКА УДАЛЕНИЯ ПОЛЬЗОВАТЕЛЯ------------------------------------------------
