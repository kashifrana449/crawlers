from datetime import date, datetime

from sqlalchemy import Column, Integer, String, DATETIME, DATE, ForeignKey

from scrapers.models.mixin import QueryMixinBigData


class Scraper(QueryMixinBigData):
    __tablename__ = 'scraper'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    baseUrl = Column(String(300))
    createdDate = Column(DATE, default=date.today)
    created = Column(DATETIME, default=datetime.now)
    modified = Column(DATETIME, default=datetime.now, onupdate=datetime.now)


class ScraperStats(QueryMixinBigData):
    __tablename__ = 'scraper_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    scraperId = Column(Integer, ForeignKey='scraper.id')
    frequency = Column(String(10))
    startTime = Column(DATETIME)
    finishTime = Column(DATETIME)
    savedRecords = Column(String(50))
    finishReason = Column(String(100))


