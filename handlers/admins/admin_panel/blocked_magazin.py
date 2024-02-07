from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api import register_commands as commands
from utils.db_api import register_commands as a_commands
from loader import dp, bot
from filters import IsAdminCheck, IsPrivate_call

# CallbackData для функции бана пользователя
block_callback = CallbackData("block_magaz", "user_id")

# Определяем количество пользователей на одной странице
USERS_PER_PAGE = 5


@dp.callback_query_handler(IsAdminCheck(), IsPrivate_call(), text='blocked_magazin')
async def get_banned_user(call: types.CallbackQuery):
    await call.answer()
    users = await commands.select_all_users()

    page_number = 1  # изначально отображаем первую страницу пользователей
    await show_users_page(call, users, page_number)


# Отображение списка пользователей на странице с заданным номером
async def show_users_page(call, users, page_number):
    start_index = (page_number - 1) * USERS_PER_PAGE
    total_pages = -(-len(users) // USERS_PER_PAGE)  # Округление количества страниц вверх
    end_index = start_index + USERS_PER_PAGE
    users_for_page = users[start_index:end_index]

    # Создание клавиатуры страницы
    kb_check_all_users = InlineKeyboardMarkup(row_width=1)
    for user in users_for_page:
        btn_profile = InlineKeyboardButton(text=f'👤{user.magazin}',
                                           callback_data=block_callback.new(user_id=user.magazin))
        kb_check_all_users.add(btn_profile)

    # Создание кнопок пагинации
    page_buttons = generate_page_buttons(page_number, total_pages)
    kb_check_all_users.row(*page_buttons)

    btn_cancel = InlineKeyboardButton(text='⬅Назад', callback_data='cancel')
    kb_check_all_users.add(btn_cancel)

    await call.message.edit_text(f'Выберите <b>Магазин/Организацию</b> для <b>Блокировки</b>:',
                                 reply_markup=kb_check_all_users)


# Генерация кнопок пагинации
def generate_page_buttons(page_number, total_pages):
    buttons = []
    if page_number > 1:
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prev_magazin_page_{page_number}"))
    buttons.append(InlineKeyboardButton(text=f'{page_number} / {total_pages}', callback_data='total_magaz'))
    if page_number < total_pages:
        buttons.append(InlineKeyboardButton(text="▶️ Вперед", callback_data=f"next_magazin_page_{page_number}"))
    return buttons


# Обработка нажатия на кнопку пагинации
@dp.callback_query_handler(lambda query: query.data.startswith(('prev_magazin', 'next_magazin')))
async def process_page_button(call: types.CallbackQuery):
    page_number = int(call.data.split('_')[-1])

    if call.data.startswith('prev_magazin'):
        page_number -= 1
    else:
        page_number += 1

    users = await commands.select_all_users()
    await show_users_page(call, users, page_number)


@dp.callback_query_handler(text_contains='block_magaz')
async def unban_user(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    callback_data = call.data.split(":")
    user_magazin = callback_data[1]
    all_shop = await commands.select_magazin(user_magazin)
    for user in all_shop:
        await a_commands.update_status_blocked(user_id=user.user_id, status='banned', reason='blocking')
    await call.message.answer(
        f'✅ Вы успешно <b>Заблокировали</b> организацию <b>{user_magazin}</b> !')
