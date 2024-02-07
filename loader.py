from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import  config
from utils.db_api.db_gino import db

# Создаем переменную бота
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Создаем хранилище для оперативной памяти
storage=MemoryStorage()

# Создаем диспетчер
dp = Dispatcher(bot, storage=storage)


__all__ = ['bot', 'storage', 'db', 'dp']