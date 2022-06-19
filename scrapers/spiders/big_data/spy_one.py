from scrapy_splash import SplashFormRequest
from scrapy.selector import Selector
from re import findall

from scrapers.spiders.base_spider import BaseSpider


class SpyOne(BaseSpider):
    name = 'Proxy from Spy-One'
    base_url = 'http://spys.one'
    urls = [
        'http://spys.one/en/free-proxy-list/',
        'http://spys.one/en/http-proxy-list/',
        'http://spys.one/en/anonymous-proxy-list/'
    ]
    select = Selector(text='')
    custom_settings = {
        'ITEM_PIPELINES': {'scrapers.pipelines.big_data.spy_one.SpyOnePipeline': 300},
        'CONCURRENT_REQUESTS': 2,
    }
    form_data = {
        'xpp': '5',
        'xf1': '0',
        'xf2': '0',
        'xf4': '0',
        'xf5': '0',
    }
    use_splash = True

    def start_requests(self):
        for url in self.urls:
            yield SplashFormRequest(url, formdata=self.form_data, endpoint='render.html', args={'wait': 5})

    def parse(self, response):
        rows = response.css('tr[onmouseover = "this.style.background=\'#002424\'"]')
        for row in rows:
            data = row.css('td')
            if data:
                item = dict()
                item['proxy'] = ':'.join(self.get_index(data, 0, self.select).css('.spy14::text').extract())
                item['proxyType'] = ''.join(self.get_index(data, 1, self.select).css('a ::text').extract())
                item['tag'] = self.get_index(data, 1, self.select).css('.spy5::text').extract_first()
                item['country'] = self.get_index(data, 3, self.select).css('.spy14::text').extract_first('')
                item['city'] = self.get_index(data, 3, self.select).css('.spy1::text').extract_first(
                    '').replace(')', '').replace('(', '')
                item['latency'] = self.get_index(data, 5, self.select).css('.spy1::text').extract_first('')
                item['speed'] = self.get_index(data, 6, self.select).css(
                    'tr[bgcolor="blue"] td::attr(width)').extract_first('')
                item['uptime'] = self.get_index(data, 8, self.select).css('.spy1 ::text').extract_first(
                    '').replace('%', '').strip()
                yield item
        # next_page = self.get_index([x.css('::attr(href)').extract_first() for x in response.css('tr.spy1xx a')
        #                             if x.css('.spy14::text').extract_first('') == 'Next page'], 0)
        # next_page = f"{self.base_url}{next_page}"
        # if next_page and next_page != response.url and next_page != self.base_url:
        #     yield SplashRequest(next_page, endpoint='render.html', args={'wait': 3})
