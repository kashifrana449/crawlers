from datetime import date, datetime
from sqlalchemy import Column, String, Integer, Date, DateTime, JSON
from scrapers.models.mixin import QueryMixinCrime


class FamilyWatchDogLocation(QueryMixinCrime):
    __tablename__ = 'fwd_location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(400), unique=True)
    bbox = Column(String(500))
    center = Column(String(500))

    created = Column(Date, default=date.today)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FWDCrimes(QueryMixinCrime):
    __tablename__ = 'fwd_crime'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    DOB = Column(Date)
    age = Column(Integer)
    sex = Column(String(20))
    race = Column(String(20))
    height = Column(String(20))
    weight = Column(String(20))
    hair = Column(String(20))
    eye = Column(String(20))
    homeAddress = Column(String(200))
    latitude = Column(String(20))
    longitude = Column(String(20))
    registeredState = Column(String(20))
    aid = Column(String(20), unique=True)
    oid = Column(String(20))
    crimeDetail = Column(JSON)
    totalCrimes = Column(Integer)
    crimes = Column(JSON)
    c = Column(String(10))
    mt = Column(String(10))
    at = Column(String(10))
    school = Column(JSON)
    key = Column(String(300))

    created = Column(Date, default=date.today)
    modified = Column(DateTime, default=datetime.utcnow)
