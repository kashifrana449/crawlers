from scrapy import Request
from json import loads, dumps, JSONDecodeError

from scrapers.spiders.base_spider import BaseSpider
from constants import CATEGORY
from scrapers.models.big_data.proxy_free_list import FreeProxyList


class Zillow(BaseSpider):
    name = 'zillow'
    category = CATEGORY['REAL_ESTATE']
    frequency = 7
    use_db_proxy = True
    base_url = 'https://www.zillow.com'

    @classmethod
    def read_proxy_list(cls):
        if hasattr(cls, 'use_db_proxy') and cls.use_db_proxy:
            cls.proxy_list = [x for x, in FreeProxyList.query.with_entities(FreeProxyList.proxy).all()]

    def start_requests(self):
        link = 'https://www.zillow.com/homes/90001_rb/'
        yield Request(link)

    def parse(self, response):
        print()