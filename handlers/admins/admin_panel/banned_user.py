import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from state.banned_users import to_banned_user
from utils.db_api import register_commands as commands
from utils.db_api import register_commands as a_commands
from loader import dp, bot
from filters import IsAdminCheck, IsPrivate_call

# ---------------------------------------БЛОК БАНА ПОЛЬЗОВАТЕЛЯ---------------------------------------------------------

# CallbackData для функции бана пользователя
ban_user_callback = CallbackData("ban_user", "user_id")

# Определяем количество пользователей на одной странице
USERS_PER_PAGE = 5


@dp.callback_query_handler(IsAdminCheck(), IsPrivate_call(), text='banned_users')
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
        famils = user.famils.replace('(', ' ')
        username = user.username.replace('(', ' ')
        btn_profile = InlineKeyboardButton(text=f'👤{famils} {username}',
                                           callback_data=ban_user_callback.new(user_id=user.user_id))
        kb_check_all_users.add(btn_profile)

    # Создание кнопок пагинации
    page_buttons = generate_page_buttons(page_number, total_pages)
    kb_check_all_users.row(*page_buttons)

    btn_cancel = InlineKeyboardButton(text='⬅Назад', callback_data='cancel')
    kb_check_all_users.add(btn_cancel)

    await call.message.edit_text(f'Выберите пользователя для <b>Бана</b>:',
                                 reply_markup=kb_check_all_users)


# Генерация кнопок пагинации
def generate_page_buttons(page_number, total_pages):
    buttons = []
    if page_number > 1:
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prev_page_{page_number}"))
    buttons.append(InlineKeyboardButton(text=f'{page_number} / {total_pages}', callback_data='total_banlist'))
    if page_number < total_pages:
        buttons.append(InlineKeyboardButton(text="▶️ Вперед", callback_data=f"next_page_{page_number}"))
    return buttons


# Обработка нажатия на кнопку пагинации
@dp.callback_query_handler(lambda query: query.data.startswith(('prev_page', 'next_page')))
async def process_page_button(call: types.CallbackQuery):
    page_number = int(call.data.split('_')[-1])

    if call.data.startswith('prev_page'):
        page_number -= 1
    else:
        page_number += 1

    users = await commands.select_all_users()
    await show_users_page(call, users, page_number)


@dp.callback_query_handler(text_contains='ban_user')
async def ban_user(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    callback_data = call.data.split(":")
    user_id = callback_data[1]
    answer = call.message.text
    global reason_banned
    reason_banned = await dp.bot.send_message(chat_id=call.message.chat.id,
                                              text=f"Введите <b>причину</b> для <b>бана</b>:",
                                              reply_to_message_id=answer)
    await state.update_data(user_id=user_id, reply_message_from_admin=reason_banned)
    await to_banned_user.text.set()


@dp.message_handler(state=to_banned_user.text)
async def reason_text(message: types.Message, state: FSMContext):
    msg_chat_banned = message.chat.id
    msg_id_banned = message.message_id
    reason = message.text
    data = await state.get_data()
    user_id = data.get('user_id')
    await a_commands.update_status_reason(user_id=int(user_id), status='baned', reason=reason)
    users = await commands.select_user_id(int(user_id))
    await message.answer(
        f'✅ Вы успешно <b>забанили</b> пользователя <b>{users.famils}</b> <b>{users.username}</b>\n🚫Причина: <code>{reason}</code>')
    # await bot.send_message(user_id, f"⚠️Администратор <b>заблокировал</b> Вас в боте\nПричина: <code>{reason}</code>")
    await state.finish()

    # Удаление сообщений после того как изменили Имя пользователю через 1 секунду
    await asyncio.sleep(1)
    await bot.delete_message(msg_chat_banned, msg_id_banned)
    await reason_banned.delete()

# -----------------------------------------КОНЕЦ БЛОКА БАНА ПОЛЬЗОВАТЕЛЯ------------------------------------------------
