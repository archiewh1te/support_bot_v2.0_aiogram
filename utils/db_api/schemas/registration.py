from sqlalchemy import Column, BigInteger, String, sql, Float

from utils.db_api.db_gino import TimedBaseModel


class Registration(TimedBaseModel):
    __tablename__ = 'registrations'
    user_id = Column(BigInteger, primary_key=True)
    tg_first_name = Column(String(200))
    tg_last_name = Column(String(200))
    famils = Column(String(100))
    username = Column(String(100))
    phone = Column(String(20))
    magazin = Column(String(100))
    status = Column(String(25))
    access = Column(BigInteger)
    reason = Column(String(100))

    query: sql.select