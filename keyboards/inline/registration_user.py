from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Кнопка Регистрации пользователя
kb_regisration_user = InlineKeyboardMarkup(row_width=1)
btn_register = InlineKeyboardButton(text='📝 Регистрация', callback_data='registration_users')

kb_regisration_user.add(btn_register)


# Кнопка отмены Регистрации пользователя
kb_cancel_registration_users = InlineKeyboardMarkup(row_width=1)
btn_cancel_register = InlineKeyboardButton(text='❌ Отмена регистрации ❌', callback_data='cancel_registration_users')

kb_cancel_registration_users.add(btn_cancel_register)