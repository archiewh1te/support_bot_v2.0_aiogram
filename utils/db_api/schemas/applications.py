from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Application(TimedBaseModel):
    __tablename__ = 'Applications'
    app_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    tg_first_name = Column(String(200))
    tg_last_name = Column(String(200))
    famils = Column(String(100))
    username = Column(String(100))
    phone = Column(String(20))
    magazin = Column(String(100))
    text_app = Column(String(1000))
    reply_text_admin = Column(String(1000))
    by_admin = Column(BigInteger)

    query: sql.select