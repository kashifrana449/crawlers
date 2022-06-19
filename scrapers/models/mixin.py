from abc import abstractmethod

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declared_attr


from scrapers.models.db import (Base, mysql_session_sports, mysql_session_real_estate, mysql_session_crime,
                                        mysql_session_country_stats, mysql_session_big_data)


class ClassProperty(object):
    def __init__(self, class_object):
        self.class_object = class_object

    def __get__(self, owner_self, owner_cls):
        return self.class_object(owner_cls)


class MixinBase(Base):

    __abstract__ = True

    session = None
    query = None

    @ClassProperty
    @abstractmethod
    def session(self):
        pass

    @declared_attr
    def __tablename__(self):
        pass

    @classmethod
    def get_by_id(cls, pk):
        return cls.query.get(pk).first()

    @classmethod
    def get_all(cls, pk):
        return cls.query.all()

    @classmethod
    def save(cls, instance):
        row_id = ''
        try:
            cls.session.add(instance)
            cls.session.commit()
        except SQLAlchemyError as e:
            cls.session.rollback()
            print('Error:', e)

    @classmethod
    def save_with_ignore(cls, instances):
        try:
            statement = cls.__table__.insert(values=instances)
            cls.session.execute(statement)
            cls.session.commit()
        except SQLAlchemyError as e:
            cls.session.rollback()
            print('Error:', e)

    @classmethod
    def update(cls, data, record):
        try:
            for key in data.keys():
                if hasattr(record, key) and not getattr(record, key):
                    setattr(record, key, data[key])
            cls.session.commit()
        except SQLAlchemyError as e:
            cls.session.rollback()
            print('Error: ', e)

    @classmethod
    def bulk_save_with_ignore(cls, instances):
        try:
            statement = cls.__table__.insert(values=instances, prefixes=['IGNORE'])
            cls.session.execute(statement)
            cls.session.commit()
        except SQLAlchemyError as e:
            cls.session.rollback()
            print('Error', e)

    @classmethod
    def bulk_update(cls, instances):
        try:
            cls.session.bulk_insert_mapping(cls.__table__, instances)
            cls.session.commit()
        except SQLAlchemyError as e:
            cls.session.rollback()
            print('Error', e)

    @classmethod
    def delete(cls, instance):
        try:
            cls.session.delete(instance)
            cls.session.commit()
        except SQLAlchemyError as e:
            print('Error:', e)


class QueryMixinSports(MixinBase):
    __abstract__ = True

    session = mysql_session_sports

    query = session.query_property()


class QueryMixinCountryStats(MixinBase):
    __abstract__ = True

    session = mysql_session_country_stats

    query = session.query_property()


class QueryMixinCrime(MixinBase):
    __abstract__ = True

    session = mysql_session_crime

    query = session.query_property()


class QueryMixinRealEstate(MixinBase):
    __abstract__ = True

    session = mysql_session_real_estate

    query = session.query_property()


class QueryMixinBigData(MixinBase):
    __abstract__ = True

    session = mysql_session_big_data

    query = session.query_property()

