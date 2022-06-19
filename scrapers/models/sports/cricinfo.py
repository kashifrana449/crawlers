from sqlalchemy import Column, Integer, String


from ..mixin import QueryMixinSports


class CricInfo(QueryMixinSports):
    __tablename__ = 'cricinfo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
