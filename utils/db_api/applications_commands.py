from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.applications import Application


# Быстрые команда Регистрации Пользователей
# Передача данных в таблицы БД
async def add_application(app_id: int, user_id: int, tg_first_name: str,  tg_last_name: str, famils: str, username: str, phone: int, magazin: str, text_app: str, reply_text_admin: str, by_admin: int):
    try:
        application = Application(app_id=app_id, user_id=user_id, tg_first_name=tg_first_name, tg_last_name=tg_last_name, famils=famils,
                                  username=username, phone=phone, magazin=magazin, text_app=text_app,
                                  reply_text_admin=reply_text_admin, by_admin=by_admin)
        await application.create()
    except UniqueViolationError:
        print('Заявка не добавлена')


# Функция которая добавляет айди заявки на +1
async def count_id_application():
    count = await db.func.count(Application.app_id).gino.scalar()
    return count


# Функция которая получает все айди заявок которые есть в БД
async def select_all_apps():
    apps = await Application.query.gino.all()
    return apps


# Функция которая выбирает по User_Id
async def select_app_by_user_id(user_id: int):
    registration = await Application.query.where(Application.user_id == user_id).gino.first()
    return registration


# Функция которая добавляет ответ от админа и кто ответил
async def answer_edit_reply(app_id, reply_text_admin, by_admin):
    app = await select_application(app_id)
    await app.update(reply_text_admin=reply_text_admin, by_admin=by_admin).apply()


# Функция которая выбирает заявку
async def select_application(app_id: int):
    app = await Application.query.where(Application.app_id == app_id).gino.first()
    return app



