from sqlalchemy import Column, String, Integer, Date, DateTime
from datetime import date, datetime
from scrapers.models.mixin import QueryMixinBigData


class FreeProxy(QueryMixinBigData):
    __tablename__ = 'free_proxy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(20))
    port = Column(String(10))
    code = Column(String(10))
    country = Column(String(100))
    anonymity = Column(String(100))
    google = Column(String(10))
    https = Column(String(10))
    key = Column(String(200))

    created = Column(Date, default=date.today)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
