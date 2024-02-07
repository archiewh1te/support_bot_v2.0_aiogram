import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from state import send_reply_from_admin
from utils.db_api import register_commands as commands
from loader import dp, bot
from filters import IsAdminCheck, IsPrivate_call

# ---------------------------------------------БЛОК ПО КНОПКЕ ОТВЕТИТЬ--------------------------------------------------

# CallbackData для функции ответа пользователю
replys_callback = CallbackData("admin_reply", "user_id")

# Определяем количество пользователей на одной странице
USERS_PER_PAGE = 5


@dp.callback_query_handler(IsAdminCheck(), IsPrivate_call(), text='replysfromadmin')
async def get_reply(call: types.CallbackQuery):
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
        btn_profile = InlineKeyboardButton(text=f'👤{famils} {username}',
                                           callback_data=replys_callback.new(user_id=user.user_id))
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
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prev_replys_page_{page_number}"))
    buttons.append(InlineKeyboardButton(text=f'{page_number} / {total_pages}', callback_data='total_check'))
    if page_number < total_pages:
        buttons.append(InlineKeyboardButton(text="▶️ Вперед", callback_data=f"next_replys_page_{page_number}"))
    return buttons


# Обработка нажатия на кнопку пагинации
@dp.callback_query_handler(lambda query: query.data.startswith(('prev_replys', 'next_replys')))
async def process_page_button(call: types.CallbackQuery):
    page_number = int(call.data.split('_')[-1])

    if call.data.startswith('prev_replys'):
        page_number -= 1
    else:
        page_number += 1

    users = await commands.select_all_users()
    await show_users_page(call, users, page_number)


@dp.callback_query_handler(text_contains='admin_reply')
async def reply_from_admins(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    global reply_message_admin
    callback_data = call.data.split(":")
    user_id = callback_data[1]
    users = await commands.select_registration_by_user_id(int(user_id))
    answer = call.message.text
    reply_message_admin = await dp.bot.send_message(chat_id=call.message.chat.id,
                                                    text=f"Введите текст для <b>{users.famils}</b> <b>{users.username}</b> :",
                                                    reply_to_message_id=answer)
    await state.update_data(user_id=user_id, reply_message_from_admin=reply_message_admin)
    await send_reply_from_admin.text.set()


@dp.message_handler(state=send_reply_from_admin.text)
async def get_reply_text(message: types.Message, state: FSMContext):
    global msg_replys_admin
    global message_chat_replytext
    global message_id_replytext
    text = message.text
    message_chat_replytext = message.chat.id
    message_id_replytext = message.message_id
    data = await state.get_data()
    user_id = data.get('user_id')
    msg_replys_admin = await message.reply('✅ Вы успешно отправили ответ!')
    await dp.bot.send_message(chat_id=user_id,
                              text=f"💬 Новое уведомление!\nСообщение от тех.поддержки:\n\n<b>{text}</b>")
    await state.finish()

    # Удаление сообщений после того как отправили пользователю через 1 секунду
    await asyncio.sleep(1)
    await reply_message_admin.delete()
    await bot.delete_message(message_chat_replytext, message_id_replytext)
    await msg_replys_admin.delete()
# ---------------------------------------КОНЕЦ БЛОКА ПО КНОПКЕ ОТВЕТИТЬ-------------------------------------------------
