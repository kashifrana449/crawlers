from datetime import date, datetime
from sqlalchemy import Column, String, Integer, Float, Date, DateTime

from scrapers.models.mixin import QueryMixinBigData


class SpyOne(QueryMixinBigData):
    __tablename__ = "spy_one"

    id = Column(Integer, primary_key=True, autoincrement=True)
    proxy = Column(String(50), unique=True)
    proxyType = Column(String(20))
    tag = Column(String(100))
    country = Column(String(100))
    city = Column(String(100))
    latency = Column(Float)
    speed = Column(Integer)
    key = Column(String(50), unique=True)
    created = Column(Date, default=date.today)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
