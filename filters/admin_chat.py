from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data import config
from utils.db_api import admins_commands

# настраиваемый фильтр для приватного чата с ботом (для Администраторов)
class IsAdminCheck(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if await admins_commands.select_admin(user_id=message.from_user.id):
            return True
        else:
            await message.answer('⛔️Вы не Администратор! Данная команда не доступна⛔️')


# Проверка айди в data.config и в БД
# class IsAdminCheck(BoundFilter):
#     async def check(self, message: types.Message) -> bool:
#         if message.from_user.id in config.admins:
#             return True
#         else:
#             return await admins_commands.select_admin(user_id=message.from_user.id)


# настраиваемый фильтр для приватного чата с ботом (onlu CallbackQuery)
# class IsAdmincallback(BoundFilter):
#     async def check(self, message: types.Message) -> bool:
#         if message.from_user.id in config.admins:
#             return True
#         else:
#             return await admins_commands.select_admin(user_id=call.from_user.id)