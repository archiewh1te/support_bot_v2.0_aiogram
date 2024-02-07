from aiogram.dispatcher.filters.state import State, StatesGroup


class FSM_Notice_admin(StatesGroup):
    text = State()


