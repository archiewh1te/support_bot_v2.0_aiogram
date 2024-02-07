from asyncpg import UniqueViolationError

from utils.db_api.schemas.registration import Registration


# Быстрые команда Регистрации Пользователей
# Передача данных в таблицы БД
async def new_registration(user_id: int, tg_first_name: str, tg_last_name: str, famils: str, username: str, phone: int,
                           magazin: str, status: str, access: int, reason: str):
    try:
        registration = Registration(user_id=user_id, tg_first_name=tg_first_name, tg_last_name=tg_last_name,
                                    famils=famils, username=username, phone=phone, magazin=magazin, status=status,
                                    access=access, reason=reason)
        await registration.create()
    except UniqueViolationError:
        print('Пользователь не добавлен, так как уже зарегистрирован!!!')


# Функция которая выбирает по статусу Актив
async def select_registration():
    registration = await Registration.query.where(Registration.status == 'active').gino.first()
    return registration


# Функция которая получает всех Пользователей которые есть в БД
async def select_all_users():
    users = await Registration.query.gino.all()
    return users


async def select_all_users2():
    distinct_users = await Registration.distinct(Registration.user_id, Registration.magazin, Registration.status).gino.all()
    return distinct_users


# Функция которая выбирает по User_Id
async def select_user_id(user_id: int):
    registration = await Registration.query.where(Registration.user_id == user_id).gino.first()
    return registration


# Функция которая выбирает по номеру телефона Пользователя
async def select_phone(phone: int):
    registration = await Registration.query.where(Registration.phone == phone).gino.first()
    return registration


# Функция которая выбирает по Фамилии Пользователя
async def select_famils(famils: str):
    registration = await Registration.query.where(Registration.famils == famils).gino.first()
    return registration


# Функция которая выбирает по имени Пользователя
async def select_registration_by_username(username: str):
    registration = await Registration.query.where(Registration.username == username).gino.first()
    return registration


# Функция которая выбирает по организации Пользователя
async def select_magazin(magazin: str):
    registration = await Registration.query.where(Registration.magazin == magazin).gino.all()
    return registration


# Функция которая подтвержадет регистрацию (пока не используется)
async def accept_registration(user_id: int):
    registration = await select_user_id(user_id)
    await registration.update(status='accepted').apply()


# Функция которая выбирает Пользователя
async def select_user(user_id):
    user = await Registration.query.where(Registration.user_id == user_id).gino.first()
    return user


# Функция которая обновляет Статус Пользователя
async def update_status_reason(user_id, status, reason):
    user = await select_user(user_id)
    await user.update(status=status, reason=reason).apply()


async def update_status_blocked(user_id, status, reason):
    user = await select_user(user_id)
    await user.update(status=status, reason=reason).apply()


# Функция которая обновляет доступ Пользователя
async def update_access(user_id, access):
    user = await select_user(user_id)
    await user.update(access=access).apply()


# Функция которая обновляет причину бана Пользователя
async def update_reason(user_id, reason):
    user = await select_user(user_id)
    await user.update(reason=reason).apply()


# Функция которая удаляет Пользователя из БД
async def delete_user(user_id):
    user = await select_user(user_id)
    await user.delete()


# Функция которая обновляет Магазин Пользователя
async def update_magazin(user_id, magazin):
    user = await select_user(user_id)
    await user.update(magazin=magazin).apply()


# Функция которая обновляет Фамилию Пользователя
async def update_famils(user_id, famils):
    user = await select_user(user_id)
    await user.update(famils=famils).apply()


# Функция которая обновляет Имя Пользователя
async def update_username(user_id, username):
    user = await select_user(user_id)
    await user.update(username=username).apply()


# Функция которая обновляет Номер телефона Пользователя
async def update_phone(user_id, phone: int):
    user = await select_user(user_id)
    await user.update(phone=phone).apply()
