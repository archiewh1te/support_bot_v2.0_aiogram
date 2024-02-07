from aiogram.dispatcher.filters.state import StatesGroup, State


class answer_from_admins(StatesGroup):
    text = State()
    state = State()
    photo = State()



