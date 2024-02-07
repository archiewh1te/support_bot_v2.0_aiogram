from aiogram.dispatcher.filters.state import StatesGroup, State


# Отправка заявки от пользователя
class send_app_from_user(StatesGroup):
    text = State()
    state = State()
    photo = State()