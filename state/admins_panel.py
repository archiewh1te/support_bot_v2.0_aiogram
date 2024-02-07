from aiogram.dispatcher.filters.state import StatesGroup, State


# для Админ панели
class AdminPanel(StatesGroup):
    text = State()
    state = State()
    photo = State()