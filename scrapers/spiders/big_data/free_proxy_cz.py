from scrapy_splash import SplashRequest
from scrapy import Request
from scrapy.selector import Selector
from re import findall
import base64

from scrapers.models.big_data.spy_one import SpyOne
from scrapers.spiders.base_spider import BaseSpider


class FreeProxyCZ(BaseSpider):
    name = 'Proxy from free-proxy-cz'
    base_url = 'http://free-proxy.cz'
    custom_settings = {
        'ITEM_PIPELINES': {'scrapers.pipelines.big_data.free_proxy_cz.FreeProxyCZPipeline': 300},
        'RETRY_TIMES': 25,
    }
    use_db_proxy = True
    select = Selector(text='')
    headers = {
        'Host': 'free-proxy.cz',
        'Referer': 'https://www.google.com/',
    }

    @classmethod
    def read_proxy_list(cls):
        records = SpyOne.query.with_entities(SpyOne.proxy).filter(SpyOne.proxyType == 'HTTP').order_by(SpyOne.id.desc())
        cls.proxy_list = [x.proxy for x in records]

    def start_requests(self):
        url = 'http://free-proxy.cz/en/'
        yield SplashRequest(url, meta={'splash': {'wait': 2, 'timeout': 5, 'headers': self.headers}})

    def parse(self, response):
        rows = response.css('#proxy_list tbody tr')
        for row in rows:
            item = dict()
            data = row.css('td')
            ip = self.get_index(data, 0, self.select).css('::text').extract_first('').replace(
                'document.write(Base64.decode("', '').replace('))', '')
            item['ip'] = base64.b64decode(ip).decode('utf8')
            item['port'] = self.get_index(data, 1, self.select).css('::text').extract_first()
            item['protocol'] = self.get_index(data, 2, self.select).css('::text').extract_first()
            item['country'] = (self.get_index(data, 3, self.select).css('a::text').extract_first()
                               or self.get_index(data, 3, self.select).css('img::attr(alt)').extract_first())
            item['region'] = self.get_index(data, 4, self.select).css('::text').extract_first()
            item['city'] = self.get_index(data, 5, self.select).css('::text').extract_first()
            item['anonymity	'] = self.get_index(data, 6, self.select).css('::text').extract_first()
            item['speed'] = self.get_index(data, 7, self.select).css('small::text'
                                                                     ).extract_first('').replace('kB/s', '').strip()
            item['UpTime'] = self.get_index(data, 8, self.select).css('small::text'
                                                                      ).extract_first('').replace('%', '').strip()
            item['response'] = self.get_index(data, 9, self.select).css('small::text'
                                                                        ).extract_first('').replace('ms', '').strip()
            yield item
        next_page = f"{self.base_url}{self.get_index(response.css('.paginator a::attr(href)').extract(), -1, '')}"
        if next_page and next_page != self.base_url and next_page != response.url:
            yield Request(next_page, headers=self.headers, meta={'max_retry_times': 25})
