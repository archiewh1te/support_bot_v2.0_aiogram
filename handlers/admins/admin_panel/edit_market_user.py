import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from state.edit_all_users import edit_market_user
from utils.db_api import register_commands as commands
from utils.db_api import register_commands as a_commands
from loader import dp, bot
from filters import IsAdminCheck, IsPrivate_call

# -------------------------------------БЛОК РЕДАКТИРОВАНИЯ МАГАЗИНА ПОЛЬЗОВАТЕЛЯ----------------------------------------

# CallbackData для функции изменения магазина или организации пользователя
editmarket_callback = CallbackData("edit_market", "user_id")

# Определяем количество пользователей на одной странице
USERS_PER_PAGE = 5


@dp.callback_query_handler(IsAdminCheck(), IsPrivate_call(), text='edit_market_users')
async def get_edit_market_users(call: types.CallbackQuery):
    await call.answer()
    users = await commands.select_all_users()

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
        btn_profile = InlineKeyboardButton(text=f'👤{famils} {username} ',
                                           callback_data=editmarket_callback.new(user_id=user.user_id))
        kb_check_all_users.add(btn_profile)

    # Создание кнопок пагинации
    total_pages = -(-len(users) // USERS_PER_PAGE)  # Округление количества страниц вверх
    page_buttons = generate_page_buttons(page_number, total_pages)
    kb_check_all_users.row(*page_buttons)

    btn_cancel = InlineKeyboardButton(text='⬅Назад ', callback_data='cancel')
    kb_check_all_users.add(btn_cancel)
    await call.message.edit_text('<b>Выберите пользователя:</b>', reply_markup=kb_check_all_users)


# Генерация кнопок пагинации
def generate_page_buttons(page_number, total_pages):
    buttons = []
    if page_number > 1:
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prev_market_page_{page_number}"))
    buttons.append(InlineKeyboardButton(text=f'{page_number} / {total_pages}', callback_data='total_market'))
    if page_number < total_pages:
        buttons.append(InlineKeyboardButton(text="▶️ Вперед", callback_data=f"next_market_page_{page_number}"))
    return buttons


# Обработка нажатия на кнопку пагинации
@dp.callback_query_handler(lambda query: query.data.startswith(('prev_market', 'next_market')))
async def process_page_button(call: types.CallbackQuery):
    page_number = int(call.data.split('_')[-1])

    if call.data.startswith('prev_market'):
        page_number -= 1
    else:
        page_number += 1

    users = await commands.select_all_users()
    await show_users_page(call, users, page_number)


@dp.callback_query_handler(text_contains='edit_market')
async def edit_market(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    callback_data = call.data.split(":")
    print(callback_data)
    user_id = callback_data[1]
    users = await commands.select_registration_by_user_id(int(user_id))
    answer = call.message.text
    global edit_market
    edit_market = await dp.bot.send_message(chat_id=call.message.chat.id,
                                            text=f"Введите Магазин/Организацию для <b>{users.famils}</b> <b>{users.username}</b> :",
                                            reply_to_message_id=answer)
    await state.update_data(user_id=user_id, reply_message_from_admin=edit_market)
    await edit_market_user.text.set()


@dp.message_handler(state=edit_market_user.text)
async def get_edit_text(message: types.Message, state: FSMContext):
    global msg_chat_market, msg_id_market
    msg_chat_market = message.chat.id
    msg_id_market = message.message_id
    text = message.text
    data = await state.get_data()
    user_id = data.get('user_id')
    await a_commands.update_magazin(user_id=int(user_id), magazin=text)
    users = await commands.select_registration_by_user_id(int(user_id))
    await message.answer(f'✅ Вы успешно сменили <b>Магазин/Организацию</b> для пользователя <b>{users.famils}</b> <b>{users.username}</b> на <b>{text}</b>')
    await state.finish()

    # Удаление сообщений после того как изменили Имя пользователю через 1 секунду
    await asyncio.sleep(1)
    await bot.delete_message(msg_chat_market, msg_id_market)
    await edit_market.delete()


# -------------------------------------КОНЕЦ БЛОКА РЕДАКТИРОВАНИЯ МАГАЗИНА----------------------------------------------
