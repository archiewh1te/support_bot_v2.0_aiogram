from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from filters import IsAdminCheck, IsPrivate_call


# ----------------------------------------- БЛОК СПИСКА ОБЫЧНЫХ КОМАНД -------------------------------------------------
# при нажатии на кнопку Cписок команд
@dp.callback_query_handler(IsAdminCheck(), IsPrivate_call(), text='list_cmd')
async def get_list_command(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    kb_delete_list_cmd = InlineKeyboardMarkup(row_width=1)
    btn_del_list_cmd = InlineKeyboardButton(text='🗑 Удалить сообщение', callback_data='del_list_cmd')
    kb_delete_list_cmd.add(btn_del_list_cmd)
    global message_cmd_list
    message_cmd_list = await call.message.answer(f'<b>Команды админа:</b>\n'
                                                 f'<code>/ответ id ТЕКСТ </code> - <b>ответить пользователю от имени '
                                                 f'бота</b>\n'
                                                 f'<code>/бан id причина </code> - <b>забанить пользователя у бота</b>\n'
                                                 f'<code>/разбан id </code> - <b>снять бан пользователя</b>\n'
                                                 f'<code>/нотис </code> - <b>отправить уведомление всем сотрудникам ТП</b>\n'
                                                 f'<code>/профиль ID-Пользователя </code> - <b>Посмотреть профиль '
                                                 f'пользователя</b>\n'
                                                 f'<code>/флаг ID-Администратора </code> - <b>Дать права '
                                                 f'Администратора</b>\n'
                                                 f'<code>/унфлаг ID-Администратора </code> - <b>Снять права '
                                                 f'Администратора</b>\n'
                                                 f'<code>/магазин ID-Пользователя НазваниеОрганизации </code> - '
                                                 f'<b>Сменить организацию у пользователя</b>\n'
                                                 f'<code>/удалить ID-Пользователя </code> - <b>Удалить пользователя из БД</b>\n'
                                                 f'<code>/фамилия ID-Пользователя Фамилия_Пользователя</code> - <b>Сменить Фамилию у пользователя</b>\n'
                                                 f'<code>/имя ID-Пользователя Фамилия_Пользователя</code> - <b>Сменить Имя у пользователя</b>\n'
                                                 f'<code>/номер ID-Пользователя Номер_Пользователя</code> - <b>Сменить номер у пользователя</b>\n'
                                                 f'<code>/applist ID-Заявки</code> - <b>Узнать информацию по заявке</b>\n'
                                                 f'<code>/list</code> - <b>Вывод всех айди заявок</b>\n'
                                                 f'<code>/sendall</code> - <b>Отправить всем пользователям уведомление</b>\n'
                                                 f'<code>/paneladm</code> - <b>Панель Администратора</b>',
                                                 reply_markup=kb_delete_list_cmd)


# удаление сообщения по инлаин кнопке
@dp.callback_query_handler(text_contains='del_list_cmd')
async def get_del_message_info(call: types.CallbackQuery):
    await message_cmd_list.delete()
# ------------------------------------------------КОНЕЦ БЛОКА СПИСКА ОБЫЧНЫХ КОМАНД-------------------------------------
