from scrapy import Request

from scrapers.spiders.base_spider import BaseSpider


class Proxy(BaseSpider):
    name = 'Proxy from free-proxy'
    base_url = 'https://free-proxy-list.net/'
    custom_settings = {
        'ITEM_PIPELINES': {'scrapers.pipelines.big_data.free_proxy.FreeProxyPipeline': 300},
    }

    def start_requests(self):
        yield Request(self.base_url)

    def parse(self, response):
        rows = response.css('.table.table-striped.table-bordered tbody tr')
        for row in rows:
            detail_list = row.css('td::text').extract()
            if detail_list:
                item = dict()
                item['ip'] = self.get_index(detail_list, 0, '').strip()
                item['port'] = self.get_index(detail_list, 1, '').strip()
                item['code'] = self.get_index(detail_list, 2, '').strip()
                item['country'] = self.get_index(detail_list, 3, '').strip()
                item['anonymity'] = self.get_index(detail_list, 4, '').strip()
                item['google'] = self.get_index(detail_list, 5, '').strip()
                item['https'] = 'https' if self.get_index(detail_list, 6, '').strip().upper() == 'YES' else 'http'
                yield item
