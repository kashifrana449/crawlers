from sqlalchemy import Column, String, Integer
from scrapers.models.mixin import QueryMixinCountryStats


class UsStates(QueryMixinCountryStats):
    __tablename__ = 'states_us'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stateName = Column(String(200))
    stateId = Column(String(50))


class UsCounties(QueryMixinCountryStats):
    __tablename__ = 'county_us'

    id = Column(Integer, primary_key=True, autoincrement=True)
    countyName = Column(String(100))
    fips = Column(String(30))
    stateId = Column(String(30))


class UsCities(QueryMixinCountryStats):
    __tablename__ = 'cities_us'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cityName = Column(String(200))
    incorporated = Column(String(20))
    density = Column(String(20))
    latitude = Column(String(30))
    longitude = Column(String(30))
    zips = Column(String(100))
    population = Column(String(20))
    population_proper = Column(String(20))
    source = Column(String(50))
    timezone = Column(String(100))
    stateId = Column(String(50))
