from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


# Создание таблицы админов
class Admins(TimedBaseModel):
    __tablename__ = 'admins'
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    user_name = Column(String(100))
    status = Column(String(30))
    flag = Column(String(30))
    access = Column(BigInteger)

    query: sql.select

