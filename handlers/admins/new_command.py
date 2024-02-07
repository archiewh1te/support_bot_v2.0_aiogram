from filters import IsPrivate, IsAdminCheck
from loader import dp, bot
from aiogram import types
from data.config import cfg
from utils.db_api import admins_commands as b_commands, applications_commands
from utils.db_api import register_commands as a_commands

lvl1name = cfg['1lvl_adm_name']
lvl2name = cfg['2lvl_adm_name']
lvl3name = cfg['3lvl_adm_name']
devid = cfg['dev_id']


def extract_arg(arg):
    return arg.split()[1:]


# Новые админские команды
# Команда ответа пользователям
@dp.message_handler(IsAdminCheck(), commands=['ответ', 'ot'])
async def admin_ot(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) >= 2:
            chatid = str(args[0])
            args.pop(0)
            answer = ""
            for ot in args:
                answer += ot + " "
            await message.reply('✅ Вы успешно отправили сообщение пользователю!')
            await bot.send_message(chatid,
                                   f"💬 Новое уведомление!\nСообщение от сотрудника тех.поддержки:\n\n<b>{answer}</b>")
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/ответ 516712732 Ваш ответ</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid, f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на доступ Пользователю для ответа на сообщения от имени Тех.Поддержки
@dp.message_handler(IsAdminCheck(), commands=['доступ', 'access'])
async def get_users_giveaccess(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 2:
            uid = int(args[0])
            access = int(args[1])
            outmsg = ""
            if await a_commands.select_user(uid):
                if access == 0:
                    outmsg = "✅ Вы успешно сняли все доступы с этого человека!"
                elif access == 1:
                    outmsg = f"✅ Вы успешно выдали доступ <b>{lvl1name}</b> данному человеку!"
                elif access == 2:
                    outmsg = f"✅ Вы успешно выдали доступ <b>{lvl2name}</b> данному человеку!"
                elif access == 3:
                    outmsg = f"✅ Вы успешно выдали доступ <b>{lvl3name}</b> данному человеку!"
                else:
                    await message.reply('⚠️ Максимальный уровень доступа: <b>3</b>')
                    return
                await a_commands.update_access(access=access, user_id=uid)
                await message.reply(outmsg)
                return
            else:
                await message.reply("⚠️Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/доступ 516712372 1</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на бан Пользователя
@dp.message_handler(IsPrivate(), IsAdminCheck(), commands=['бан', 'ban'])
async def get_users_ban(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 2:
            uid = int(args[0])
            reason = args[1]
            if await a_commands.select_user(uid):
                await a_commands.update_status_reason(user_id=uid, status='baned', reason=reason)
                await message.reply(f'✅ Вы успешно забанили этого пользователя\nПричина: <code>{reason}</code>')
                # await bot.send_message(uid, f"⚠️Администратор <b>заблокировал</b> Вас в боте\nПричина: <code>{
                # reason}</code>")
                return
            else:
                await message.reply("⚠️Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️Укажите аргументы команды\nПример: <code>/бан 51623722 Причина</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на разбан Пользователя
@dp.message_handler(IsPrivate(), IsAdminCheck(), commands=['разбан', 'unban'])
async def get_users_unban(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 1:
            uid = int(args[0])
            if await a_commands.select_user(uid):
                await a_commands.update_status_reason(user_id=uid, status='active', reason='no reason')
                await message.reply(f'✅ Вы успешно <b>разблокировали</b> этого пользователя')
                # await bot.send_message(uid, f"⚠️ Администратор <b>разблокировал</b> Вас в боте!")
                return
            else:
                await message.reply("⚠️ Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/разбан 516272834</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на получение айдидшника пользователя
@dp.message_handler(IsPrivate(), IsAdminCheck(), commands=['айди', 'id'])
async def admin_id(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 1:
            username = args[0]
            user = await a_commands.select_registration_by_username(username)
            if user:
                await message.reply(f"🔎 Информация:\n"
                                    f"👤 Никнейм: {user.username}\n"
                                    f"🆔 Айди пользователя {user.user_id}\n")
            else:
                await message.reply("⚠️ Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/айди nosemka</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на просмотр профиля Пользователя
@dp.message_handler(IsAdminCheck(), commands=['профиль', 'profile'])
async def get_profile_admin(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 1:
            uid = int(args[0])
            users = await a_commands.select_user(uid)
            if users:
                await message.answer(f'🔎<b>Информарция о пользователе:</b>\n'
                                     f'<b>📍NickName</b>:{users.tg_first_name}\n'
                                     f'<b>🆔ID:</b> {users.user_id}\n'
                                     f'<b>🕵️‍Статус</b>: {users.status}\n'
                                     f'<b>🔑Доступ</b>: {users.access}\n'
                                     f'<b>👤Фамилия</b>: {users.famils}\n'
                                     f'<b>👤Имя</b>: {users.username}\n'
                                     f'<b>📞Телефон</b>: {users.phone}\n'
                                     f'<b>🏢Магазин</b>: {users.magazin}\n')
            else:
                await message.reply("⚠️ Этого айдишника <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/профиль айди_пользователя</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на право администратирования
@dp.message_handler(IsAdminCheck(), commands=['флаг', 'flag'])
async def get_users_unban(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 1:
            uid = int(args[0])
            if await b_commands.select_admin(uid):
                await b_commands.update_flag(user_id=uid, flag='admin')
                await message.reply(f'✅ Вы успешно дали доступ <b>Администратора</b> для этого пользователя')
                await bot.send_message(uid,
                                       f"⚠️ Администратор <b>дал вам права</b> ознакомтесь со списком доступных команд <code>/clist</code> !")
                return
            else:
                await message.reply("⚠️ Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/флаг 516272834</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на снятие права администратирования
@dp.message_handler(IsPrivate(), IsAdminCheck(), commands=['унфлаг', 'unflag'])
async def get_users_unban(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 1:
            uid = int(args[0])
            if await b_commands.select_admin(uid):
                await b_commands.update_flag(user_id=uid, flag='noadmin')
                await message.reply(f'✅ Вы успешно сняли доступ <b>Администратора</b> с этого пользователя')
                await bot.send_message(uid, f"⚠️ Администратор <b>снял с вас права</b>!")
                return
            else:
                await message.reply("⚠️ Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/унфлаг 516272834</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на смену магазина у пользователя
@dp.message_handler(IsPrivate(), IsAdminCheck(), commands=['магазин', 'magazin'])
async def get_edit_magazin(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 2:
            uid = int(args[0])
            magazin = args[1]
            if await a_commands.select_user(uid):
                await a_commands.update_magazin(user_id=uid, magazin=magazin)
                await message.reply(
                    f'✅ Вы успешно сменили  <b>Организацию</b> для этого пользователя на <code>{magazin}</code>')
                return
            else:
                await message.reply("⚠️ Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply(
                '⚠️ Укажите аргументы команды\nПример: <code>/магазин 51623722 НазваниеОрганизации</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на удаление Пользователя из БД
@dp.message_handler(IsAdminCheck(), commands=['удалить', 'del'])
async def get_profile_delete(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 1:
            uid = int(args[0])
            if await a_commands.select_user(uid):
                await a_commands.delete_user(user_id=uid)
                await message.reply(f'✅ Вы успешно удалили Пользователя с 🆔<code>{uid}</code>')
            else:
                await message.reply("⚠️ Этого айдишника <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/удалить айди_пользователя</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на смену Фамилии у пользователя
@dp.message_handler(IsPrivate(), IsAdminCheck(), commands=['фамилия', 'famil'])
async def get_edit_magazin(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 2:
            uid = int(args[0])
            famils = args[1]
            if await a_commands.select_user(uid):
                await a_commands.update_famils(user_id=uid, famils=famils)
                await message.reply(
                    f'✅ Вы успешно сменили  <b>Фамилию</b> для этого пользователя на <code>{famils}</code>')
                return
            else:
                await message.reply("⚠️ Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply(
                '⚠️ Укажите аргументы команды\nПример: <code>/фамилия 51623722 фамилия_пользователя</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на смену Имени у пользователя
@dp.message_handler(IsPrivate(), IsAdminCheck(), commands=['имя', 'name'])
async def get_edit_magazin(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 2:
            uid = int(args[0])
            username = args[1]
            if await a_commands.select_user(uid):
                await a_commands.update_username(user_id=uid, username=username)
                await message.reply(
                    f'✅ Вы успешно сменили  <b>Имя</b> для этого пользователя на <code>{username}</code>')
                return
            else:
                await message.reply("⚠️ Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/имя 51623722 имя_пользователя</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


@dp.message_handler(IsPrivate(), IsAdminCheck(), commands=['номер', 'number'])
async def get_users_ban(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 2:
            uid = int(args[0])
            number = args[1]
            if await a_commands.select_user(uid):
                await a_commands.update_phone(user_id=uid, phone=number)
                await message.reply(
                    f'✅ Вы успешно сменили <b>номер телефона</b> этого пользователя на <code>{number}</code>')
                return
            else:
                await message.reply("⚠️ Этого пользователя <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/номер 51623722 номер_телефона</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на просмотр заявок
@dp.message_handler(IsAdminCheck(), commands=['список', 'applist'])
async def get_info_app(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 1:
            id = int(args[0])
            app = await applications_commands.select_application(id)
            if app:
                await message.answer(f'🔎<b>Информарция о Заявке:</b>\n'
                                     f'<b>🆔Номер заявки:</b> {app.app_id}\n'
                                     f'<b>📍NickName</b>: {app.tg_first_name}\n'
                                     f'<b>🆔ID:</b> {app.user_id}\n'
                                     f'<b>👤Фамилия</b>: {app.famils}\n'
                                     f'<b>👤Имя</b>: {app.username}\n'
                                     f'<b>📞Телефон</b>: {app.phone}\n'
                                     f'<b>🏢Магазин</b>: {app.magazin}\n'
                                     f'<b>Текст</b>: <code>{app.text_app}</code>\n'
                                     f'<b>Кто отвечал:</b> {app.by_admin}\n'
                                     f'<b>Ответ от ТП</b>: <code>{app.reply_text_admin}</code>\n')

            else:
                await message.reply("⚠️ Этого айдишника заявки <b>не</b> существует!")
                return
        else:
            await message.reply('⚠️ Укажите аргументы команды\nПример: <code>/applist ID_Заявки</code>')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на вывод всех айдишников заявок
@dp.message_handler(IsAdminCheck(), commands=['list'])
async def get_list_app(message: types.Message):
    try:
        apps = await applications_commands.select_all_apps()
        list = []
        for app in apps:
            list.append(app.app_id)
        list = ', '.join([str(item) for item in list])
        print(list)
        await message.answer(f'🔎<b>Список ID заявок:</b>\n'
                             f'<b>📍ID:</b> {list}\n')

    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! <b>Ошибка!</b> Не переживайте, ошибка уже <b>отправлена</b> разработчику.")
        await bot.send_message(devid,
                               f"Случилась <b>ошибка</b> в чате <b>{cid}</b>\nСтатус ошибки: <code>{e}</code>")


# Команда на вывод список листа команд для администраторов
@dp.message_handler(IsAdminCheck(), commands=['клист', 'clist'])
async def admin_commandlist(message: types.Message):
    await message.answer(f'<b>Команды админа:</b>\n'
                         f'<code>/ответ id ТЕКСТ </code> - <b>ответить пользователю от имени бота</b>\n'
                         f'<code>/бан id причина </code> - <b>забанить пользователя у бота</b>\n'
                         f'<code>/разбан id </code> - <b>снять бан пользователя</b>\n'
                         f'<code>/нотис </code> - <b>отправить уведомление всем сотрудникам ТП</b>\n'
                         f'<code>/профиль ID-Пользователя </code> - <b>Посмотреть профиль пользователя</b>\n'
                         f'<code>/флаг ID-Администратора </code> - <b>Дать права Администратора</b>\n'
                         f'<code>/унфлаг ID-Администратора </code> - <b>Снять права Администратора</b>\n'
                         f'<code>/магазин ID-Пользователя НазваниеОрганизации </code> - <b>Сменить организацию у пользователя</b>\n'
                         f'<code>/удалить ID-Пользователя </code> - <b>Удалить пользователя из БД</b>\n'
                         f'<code>/фамилия ID-Пользователя Фамилия_Пользователя</code> - <b>Сменить Фамилию у пользователя</b>\n'
                         f'<code>/имя ID-Пользователя Фамилия_Пользователя</code> - <b>Сменить Имя у пользователя</b>\n'
                         f'<code>/номер ID-Пользователя Номер_Пользователя</code> - <b>Сменить номер у пользователя</b>\n'
                         f'<code>/applist ID-Заявки</code> - <b>Узнать информацию по заявке</b>\n'
                         f'<code>/list</code> - <b>Вывод всех айди заявок</b>\n'
                         f'<code>/sendall</code> - <b>Отправить всем пользователям уведомление</b>\n'
                         f'<code>/paneladm</code> - <b>Панель Администратора</b>')

# Новые админские команды
# # Команда на просмотр профиля Юзера
# @dp.message_handler(IsPrivate(), commands=['профильадм', 'profileadm'])
# async def get_profile_admin(message: types.Message):
#     args = extract_arg(message.text)
#     if len(args) == 2:
#         uid = int(args[0])
#         admin = b_commands.select_admin(user_id=uid)
#         await message.answer(f'ID: {admin.user_id}\n'
#                              f'first_name: {admin.first_name}\n'
#                              f'last_name: {admin.last_name}\n'
#                              f'user_name: {admin.user_name}\n'
#                              f'status: {admin.status}\n'
#                              f'flag: {admin.flag}\n'
#                              f'access: {admin.access}\n')
