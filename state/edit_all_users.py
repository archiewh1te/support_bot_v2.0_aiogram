from aiogram.dispatcher.filters.state import StatesGroup, State


class edit_famils_user(StatesGroup):
    text = State()
    state = State()
    photo = State()


class edit_name_user(StatesGroup):
    text = State()
    state = State()
    photo = State()


class edit_market_user(StatesGroup):
    text = State()
    state = State()
    photo = State()


class edit_phone_user(StatesGroup):
    text = State()
    state = State()
    photo = State()

