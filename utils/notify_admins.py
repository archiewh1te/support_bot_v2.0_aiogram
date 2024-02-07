import logging
import time

from aiogram import Dispatcher

from data.config import admins

date_now  = time.strftime("%Y-%m-%d", time.localtime())
time_now = time.strftime("%H:%M:%S", time.localtime())


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            text = (f"✅Бот запущен и готов к работе!\n"
                    f"📅Дата: {date_now}\n"
                    f"⏰Время: {time_now}")
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)