from sqlalchemy import Column, String, Integer, Date, DateTime, UniqueConstraint
from datetime import date, datetime
from scrapers.models.mixin import QueryMixinBigData


class FreeProxyCZ(QueryMixinBigData):
    __tablename__ = 'free_proxy_cz'
    __table_args__ = (UniqueConstraint('ip', 'port', 'protocol', name='free_proxy_cz_uc'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(20))
    port = Column(String(10))
    protocol = Column(String(10))
    country = Column(String(100))
    city = Column(String(100))
    anonymity = Column(String(100))
    speed = Column(String(10))
    UpTime = Column(String(10))
    response = Column(String(10))
    key = Column(String(200), unique=True)

    created = Column(Date, default=date.today)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
