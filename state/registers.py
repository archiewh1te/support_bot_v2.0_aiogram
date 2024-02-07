from aiogram.dispatcher.filters.state import StatesGroup, State

class reg(StatesGroup):
    familiya = State()
    name = State()
    magazine = State()
    phone = State()


