from datetime import date, datetime
from sqlalchemy import Integer, Column, String, Date, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from scrapers.models.mixin import QueryMixinRealEstate


# class RENzSt(QueryMixinRealEstate):
#     __tablename__ = 'real_estate_nz_st'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     propertyId = Column(String(50), unique=True)
#     propertyName = Column(String(200))
#     area = Column(String(50))
#     category = Column(String(100))
#     parking = Column(String(50))
#     publishedDate = Column(String(100))
#     bed = Column(String(50))
#     price = Column(String(50))
#     createDate = Column(Date, date.today)
#     created = Column(DateTime, default=datetime.utcnow)
#     modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ReNz(QueryMixinRealEstate):
    __tablename__ = 'real_estate_nz'

    id = Column(Integer, primary_key=True, autoincrement=True)
    propertyId = Column(String(50), unique=True)
    listingId = Column(String(50))
    propertyType = Column(String(50))
    propertyName = Column(String(200))
    area = Column(String(50))
    areaUnit = Column(String(50))
    category = Column(String(100))
    parkingOtherCount = Column(String(50))
    parkingGarageCount = Column(String(50))
    storyCount = Column(String(50))
    maxTenants = Column(String(50))
    floorArea = Column(String(50))
    bathCount = Column(String(50))
    bathEnsuiteCount = Column(String(50))
    bathWcCount = Column(String(50))
    hasSwimmingPool = Column(String(50))
    parking = Column(String(50))
    publishedDate = Column(String(100))
    bed = Column(String(50))
    streetNumber = Column(String(50))
    street = Column(String(100))
    postCode = Column(String(50))
    address = Column(String(200))
    country = Column(String(50))
    region = Column(String(100))
    district = Column(String(50))
    latitude = Column(String(50))
    longitude = Column(String(50))
    subUrb = Column(String(100))
    nearBySuburb = Column(String(String(700)))
    nearBySuburbSlugs = Column(String(700))
    offices = Column(String(700))
    agents = Column(String(700))
    schools = Column(String(700))
    additionalWebsites = Column(String(700))

    createdDate = Column(Date, default=date.today)
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RENzPricing(QueryMixinRealEstate):
    __tablename__ = 'real_estate_nz_pricing'
    __table_args__ = (UniqueConstraint('propertyKey', 'createdDate', name='real_estate_nz_pricing_uc'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(String(50))
    listingStatus = Column(String(50))
    propertyKey = Column(Integer, ForeignKey('real_estate_nz.id'))
    property = relationship(ReNz)
    createdDate = Column(Date, default=date.today)
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
