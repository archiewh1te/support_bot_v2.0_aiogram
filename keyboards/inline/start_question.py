from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb_start_question = InlineKeyboardMarkup(row_width=3)
btn_start = InlineKeyboardButton(text='✉ Задать вопрос', callback_data='start_question')
kb_start_question.add(btn_start)


kb_cancel_question = InlineKeyboardMarkup(row_width=3)
btn_cancel = InlineKeyboardButton(text='❌Отмена подачи заявки❌', callback_data='quit')
kb_cancel_question.add(btn_cancel)


kb_menu_applications = InlineKeyboardMarkup(row_width=2)
kb_add_photo = InlineKeyboardButton(text='📷Добавить фото', callback_data='add_photo')
kb_send = InlineKeyboardButton(text='⬆Отправить', callback_data='next')
kb_menu_applications.add(kb_add_photo, kb_send)
kb_cancel = InlineKeyboardButton(text='❌Отменить', callback_data='quit')
kb_menu_applications.add(kb_cancel)


kb_cancel_all = InlineKeyboardMarkup(row_width=1)
kb_cancel = InlineKeyboardButton(text='❌Отменить', callback_data='quit')
kb_cancel_all.add(kb_cancel)