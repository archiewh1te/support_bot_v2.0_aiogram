from aiogram import Dispatcher

from .private_chat import IsPrivate, IsPrivate_call
from .admin_chat import IsAdminCheck


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdminCheck)
    dp.filters_factory.bind(IsPrivate_call)
