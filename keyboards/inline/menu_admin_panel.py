from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура Админ панели
kb_adm_pnl = InlineKeyboardMarkup(row_width=3)
btn_reply = InlineKeyboardButton(text='💬 Ответить', callback_data='replysfromadmin')
btn_edit = InlineKeyboardButton(text='✏️ Изменить', callback_data='edit')
btn_profile = InlineKeyboardButton(text='👤 Профиль', callback_data='profile')
btn_notice = InlineKeyboardButton(text='📢 Нотисы', callback_data='notice')
btn_app = InlineKeyboardButton(text='📋 Заявки', callback_data='applications')
btn_cmd_list = InlineKeyboardButton(text='📃 Список команд', callback_data='list_cmd')

kb_adm_pnl.add(btn_reply, btn_edit, btn_profile, btn_notice, btn_app, btn_cmd_list)


# Клавиатура Кнопки Профиль
kb_profile_pnl = InlineKeyboardMarkup(row_width=2)
btn_check_profile = InlineKeyboardButton(text='👀 Посмотреть Профиль', callback_data='check_user_profile')
btn_del = InlineKeyboardButton(text='❌ Удалить Профиль', callback_data='delete_users')
btn_ban = InlineKeyboardButton(text='🔇 Бан', callback_data='banned_users')
btn_unban = InlineKeyboardButton(text='🔓 Разбан', callback_data='unbanusers')
btn_cancel = InlineKeyboardButton(text='⬅Назад ', callback_data='cancel')

kb_profile_pnl.add(btn_check_profile, btn_ban, btn_del, btn_unban, btn_cancel)


# Клавиатура Кнопки Изменить
kb_edit_pnl = InlineKeyboardMarkup(row_width=2)
btn_famils = InlineKeyboardButton(text='👤 Фамилию', callback_data='edit_famils_users')
btn_name = InlineKeyboardButton(text='👤 Имя', callback_data='edit_name_users')
btn_number = InlineKeyboardButton(text='📞 Номер телефона', callback_data='edit_phone_users')
btn_market = InlineKeyboardButton(text='🏪 Магазин', callback_data='edit_market_users')
btn_block = InlineKeyboardButton(text='🔓 Разблокировать', callback_data='magazin_unblock')
btn_unblock = InlineKeyboardButton(text='🚫 Заблокировать', callback_data='blocked_magazin')
btn_cancel = InlineKeyboardButton(text='⬅Назад ', callback_data='cancel')

kb_edit_pnl.row(btn_block, btn_unblock)
kb_edit_pnl.add(btn_famils, btn_name, btn_number, btn_market, btn_cancel)


# Клавиатура Кнопки Нотисы
kb_notice_pnl = InlineKeyboardMarkup(row_width=2)
btn_notice_adm = InlineKeyboardButton(text='🔈👮🏼‍♂ ️Нотис для ТП', callback_data='notice_all_admins')
btn_notice_all = InlineKeyboardButton(text='📢👥 Нотис всем юзерам', callback_data='notice_all_users')
btn_cancel = InlineKeyboardButton(text='⬅Назад ', callback_data='cancel')

kb_notice_pnl.add(btn_notice_adm, btn_notice_all, btn_cancel)


# Клавиатура Кнопки Заявки
kb_applications_pnl = InlineKeyboardMarkup(row_width=1)
btn_list_app = InlineKeyboardButton(text='📃 Список заявок', callback_data='list_app')
btn_cancel = InlineKeyboardButton(text='⬅Назад ', callback_data='cancel')

kb_applications_pnl.add(btn_list_app, btn_cancel)