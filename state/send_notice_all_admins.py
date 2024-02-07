from aiogram.dispatcher.filters.state import StatesGroup, State


# Уведомления для всех сотрудников Технической поддержки
class send_notice_alladmins(StatesGroup):
    text = State()
    state = State()
    photo = State()