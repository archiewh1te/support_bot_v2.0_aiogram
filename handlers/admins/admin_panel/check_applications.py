from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api import applications_commands
from loader import dp
from filters import IsAdminCheck, IsPrivate_call

# -------------------------------------БЛОК ВЫВОДА ВСЕХ АЙДИ И ПРОСМОТРА ЗАЯВОК-----------------------------------------

# CallbackData для функции списка заявок
listapp_callback = CallbackData("list_apps", "app_id")

# Определяем количество заявок на одной странице
APPS_PER_PAGE = 5


@dp.callback_query_handler(IsAdminCheck(), IsPrivate_call(), text='list_app')
async def get_list_app(call: types.CallbackQuery):
    await call.answer()
    apps = await applications_commands.select_all_apps()
    page_number = 1  # изначально отображаем первую страницу заявок
    await show_apps_page(call, apps, page_number)


# Отображение списка заявок на странице с заданным номером
async def show_apps_page(call, apps, page_number):
    start_index = (page_number - 1) * APPS_PER_PAGE
    total_pages = -(-len(apps) // APPS_PER_PAGE)  # Округление количества страниц вверх
    end_index = start_index + APPS_PER_PAGE
    apps_for_page = apps[start_index:end_index]

    # Создание клавиатуры страницы
    kb_check_all_apps = InlineKeyboardMarkup(row_width=1)
    for app in apps_for_page:
        btn_profile = InlineKeyboardButton(text=f'#️⃣ {app.app_id} | {app.magazin} | {app.famils} {app.username}',
                                           callback_data=listapp_callback.new(app_id=app.app_id))
        kb_check_all_apps.add(btn_profile)

    # Создание кнопок пагинации
    page_buttons = generate_page_buttons(page_number, total_pages)
    kb_check_all_apps.row(*page_buttons)

    btn_cancel = InlineKeyboardButton(text='⬅Назад', callback_data='cancel')
    kb_check_all_apps.add(btn_cancel)

    await call.message.edit_text(f'<b>Список заявок :</b>', reply_markup=kb_check_all_apps)


# Генерация кнопок пагинации
def generate_page_buttons(page_number, total_pages):
    buttons = []
    if page_number > 1:
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prev_list_{page_number}"))
    buttons.append(InlineKeyboardButton(text=f'{page_number} / {total_pages}', callback_data='total_listapp'))
    if page_number < total_pages:
        buttons.append(InlineKeyboardButton(text="▶️ Вперед", callback_data=f"next_list_{page_number}"))
    return buttons


# Обработка нажатия на кнопку пагинации
@dp.callback_query_handler(lambda query: query.data.startswith(('prev_list', 'next_list')))
async def process_page_button(call: types.CallbackQuery):
    await call.answer()
    page_number = int(call.data.split('_')[-1])

    if call.data.startswith('prev_list'):
        await call.answer()
        page_number -= 1
    else:
        page_number += 1

    apps = await applications_commands.select_all_apps()
    await show_apps_page(call, apps, page_number)


@dp.callback_query_handler(text_contains='list_apps')
async def get_check_apps(call: types.CallbackQuery):
    await call.answer()
    callback_data = call.data.split(":")
    app_id = callback_data[1]
    app = await applications_commands.select_application(int(app_id))
    kb_del_info_apps = InlineKeyboardMarkup(row_width=1)
    btn_delete_info_apps = InlineKeyboardButton(text='⬅Назад', callback_data='list_app')
    kb_del_info_apps.add(btn_delete_info_apps)
    global message_info_apps
    message_info_apps = await call.message.edit_text(text=f'🔎<b>Информарция о Заявке:</b>\n\n'
                                                          f'<b>🆔Номер заявки:</b> {app.app_id}\n'
                                                          f'<b>📍NickName</b>: {app.tg_first_name}\n'
                                                          f'<b>🆔ID:</b> {app.user_id}\n'
                                                          f'<b>👤Фамилия</b>: {app.famils}\n'
                                                          f'<b>👤Имя</b>: {app.username}\n'
                                                          f'<b>📞Телефон</b>: {app.phone}\n'
                                                          f'<b>🏢Магазин</b>: {app.magazin}\n'
                                                          f'<b>Текст</b>: <code>{app.text_app}</code>\n'
                                                          f'<b>Кто отвечал:</b> {app.by_admin}\n'
                                                          f'<b>Ответ от ТП</b>: <code>{app.reply_text_admin}</code>\n',
                                                     reply_markup=kb_del_info_apps)


# ------------------------------------------------ КОНЕЦ БЛОКА СПИСКА ЗАЯВОК -------------------------------------------
