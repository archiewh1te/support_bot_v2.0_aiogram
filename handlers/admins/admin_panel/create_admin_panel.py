from aiogram import types
from filters import IsAdminCheck, IsPrivate
from keyboards.inline import kb_adm_pnl, kb_profile_pnl, kb_edit_pnl, kb_notice_pnl, kb_applications_pnl
from loader import dp


# команда на вывод панели для Администратора
@dp.message_handler(IsAdminCheck(), IsPrivate(), commands=['paneladm'])
async def get_panel(message: types.Message):
    await message.answer('<b>👮🏼‍♂️ Меню Админ Панели</b>', reply_markup=kb_adm_pnl)


# Кнопка возращает назад на главное меню
@dp.callback_query_handler(text='cancel')
async def get_cancel(call: types.CallbackQuery):
    await call.message.edit_text('<b>👮🏼‍ Меню Админ Панели</b>', reply_markup=kb_adm_pnl)


# Меню при нажатии на кнопку Профиль
@dp.callback_query_handler(text='profile')
async def get_profile(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('<b>👤 Меню Профиль</b>', reply_markup=kb_profile_pnl)


# Меню при нажатии на кнопку Изменить
@dp.callback_query_handler(text='edit')
async def get_edit(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('<b>✏️ Меню Редактирования</b>', reply_markup=kb_edit_pnl)


# Меню при нажатии на кнопку Нотисы
@dp.callback_query_handler(text='notice')
async def get_notice(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('<b>🔈 Меню Уведомлений</b>', reply_markup=kb_notice_pnl)


# Меню при нажатии на кнопку Заявки
@dp.callback_query_handler(text='applications')
async def get_applications(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('<b>📋 Меню Заявок</b>', reply_markup=kb_applications_pnl)


