from scrapy import Spider

from scrapers.models.sports.cricinfo import CricInfo


class CricInfoSpider(Spider):
    name = 'Cric Info'

    start_urls = ['http://www.espncricinfo.com/']

    def parse(self, response):
        records = CricInfo.get_all()
        print(records)
