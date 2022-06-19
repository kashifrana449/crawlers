from sqlalchemy import Column, String, Integer

from scrapers.models.mixin import QueryMixinBigData


class FreeProxyList(QueryMixinBigData):
    __tablename__ = 'free_proxy_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    proxy = Column(String(30), unique=True)
