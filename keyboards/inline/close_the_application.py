from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура Закрытия заявки
kb_close_the_app = InlineKeyboardMarkup(row_width=2)
btn_app_closed = InlineKeyboardButton(text='✅Заявка закрыта', callback_data='app_closed')
btn_app_open = InlineKeyboardButton(text='❌Заявка открыта', callback_data='app_open')


kb_close_the_app.add(btn_app_closed, btn_app_open)