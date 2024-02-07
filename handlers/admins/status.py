from filters import IsPrivate
from loader import dp, bot
from aiogram import types
import os
import time
from data.config import cfg
from utils.db_api import admins_commands as commands

date_now = time.strftime("%Y-%m-%d", time.localtime())
time_now = time.strftime("%H:%M:%S", time.localtime())

teh_chat_id = cfg['teh_chat_id']
devid = cfg['dev_id']


@dp.message_handler(IsPrivate(), commands=['статус', 'status'], state=None)
async def admin_status(message: types.Message):
    try:
        if (message.chat.type != 'private'):
            await message.answer('Данную команду можно использовать только в личных сообщениях с ботом.')
            return
        admin = await commands.select_admin(message.from_user.id)
        if admin.flag == 'admin':
            hostname = "8.8.8.8"
            response = os.system("ping -n 3 " + hostname)
            if response == 0:
                response. = "Network Active"
                await message.answer(
                    f'🌐<b>Статус бота:</b>\n'
                    f'✅<b>Бот на связи!</b>\n'
                    f'📅Дата: {date_now}\n'
                    f'⏰Время:  {time_now}')
            else:
                pingstatus = "Network Error"
                await message.answer(
                    f'🌐<b>Статус бота:</b>\n'
                    f'❌<b>Бот не на связи!</b>\n'
                    f'📅Дата: {date_now}\n'
                    f'⏰Время:  {time_now}')

            return pingstatus
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"Упс! *Ошибка!* Не переживайте, ошибка уже *отправлена* разработчику.",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`", parse_mode='Markdown')
