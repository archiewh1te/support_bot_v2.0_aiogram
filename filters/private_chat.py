from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


# Фильтр чтобы использовать приватные сообщения в боте
class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsPrivate_call(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        return call.message.chat.type == types.ChatType.PRIVATE