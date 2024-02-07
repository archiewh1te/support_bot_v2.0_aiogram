from  asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.admins import Admins


# Быстрые команды Админов
# Передача данных в таблицы БД
async def add_admins(user_id: int, first_name: str, last_name: str, user_name: str, status: str, flag: str, access: int):
    try:
        add_admin = Admins(user_id=user_id, first_name=first_name, last_name=last_name, user_name=user_name, status=status, flag=flag, access=access)
        await add_admin.create()
    except UniqueViolationError:
        print('Пользователь не добавлен')


# Функция которая получает всех Администраторов которые есть в БД
async def select_all_admins():
     admins = await Admins.query.gino.all()
     return admins


# Функция которая выбирает Администратора из БД по флагу
async def select_admin_flag():
    admin = await Admins.query.where(Admins.flag == 'admin').gino.first()
    return admin


# Функция которая выбирает Администратора из БД по user_id
async def select_admin(user_id):
    admin = await Admins.query.where(Admins.user_id == user_id).gino.first()
    return admin


# Функуия которая обновляет юзернейм Администратора
async def update_admin_name(user_id, new_name):
    admin = await select_admin(user_id)
    await admin.update(update_name=new_name).apply()


# Функция которая обновляет статус Администратора
async def update_status(user_id, status):
    user = await select_admin(user_id)
    await user.update(status=status).apply()

# Функция которая обновляет Доступ Администратора
async def update_access(user_id, access):
    user = await select_admin(user_id)
    await user.update(access=access).apply()


# Функция которая обновляет Флаг Администратора
async def update_flag(user_id, flag):
    user = await select_admin(user_id)
    await user.update(flag=flag).apply()

