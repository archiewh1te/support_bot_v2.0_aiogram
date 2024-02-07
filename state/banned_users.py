from aiogram.dispatcher.filters.state import StatesGroup, State


class to_banned_user(StatesGroup):
    text = State()
    state = State()
    photo = State()