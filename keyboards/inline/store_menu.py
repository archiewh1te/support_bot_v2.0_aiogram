from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Первый ряд
kb_menu_magazinreply = InlineKeyboardMarkup(row_width=3)
btn_test_1 = InlineKeyboardButton(text='🏪 Магазин 1', callback_data='mag_test1')
btn_test_2 = InlineKeyboardButton(text='🏪 Магазин 2', callback_data='mag_test2')
kb_menu_magazinreply.add(btn_test_1, btn_test_2)


btn_test_3 = InlineKeyboardButton(text='🏪 Магазин 3', callback_data='mag_test3')
btn_test_4 = InlineKeyboardButton(text='🏪 Магазин 4', callback_data='mag_test4')
btn_test_5 = InlineKeyboardButton(text='🏪 Магазин 5', callback_data='mag_test5')

kb_menu_magazinreply.add(btn_test_3, btn_test_4, btn_test_5)

# Второй ряд
btn_test_6 = InlineKeyboardButton(text='🏪 Магазин 6', callback_data='mag_test6')
btn_test_7 = InlineKeyboardButton(text='🏪 Магазин 7', callback_data='mag_test7')
btn_test_8 = InlineKeyboardButton(text='🏪 Магазин 8', callback_data='mag_test8')

kb_menu_magazinreply.add(btn_test_6, btn_test_7, btn_test_8)

# Третий ряд
btn_test_9 = InlineKeyboardButton(text='🏪 Магазин 9', callback_data='mag_test9')
btn_test_10 = InlineKeyboardButton(text='🏪 Магазин 10', callback_data='mag_test10')
btn_test_11 = InlineKeyboardButton(text='🏪 Магазин 11', callback_data='mag_test11')

kb_menu_magazinreply.add(btn_test_9, btn_test_10, btn_test_11)

# Кнопка отмены регистрации в самом низу
btn_cancel_registration = InlineKeyboardButton(text='❌ Отмена регистрации ❌', callback_data='cancel_registration_users')

kb_menu_magazinreply.add(btn_cancel_registration)