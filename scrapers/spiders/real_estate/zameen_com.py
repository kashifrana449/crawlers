from scrapy import Request

from constants import CATEGORY

from scrapers.spiders.base_spider import BaseSpider


class ZameenComSpider(BaseSpider):
    name = 'zameen_com'
    category = CATEGORY['REAL_ESTATE']
    frequency = 7
    use_selenium = True
    domain = 'https://www.zameen.com'
    base_url = 'https://www.zameen.com/Homes/Lahore-1-1.html'

    custom_settings = {
        'ITEM_PIPELINES': {'pipelines.CSVPipeline': 300},
    }

    def start_requests(self):
        yield Request(self.base_url)

    def parse(self, response):
        properties = response.css('li[role="article"]') or []
        for home in properties:
            house_link = home.css('a[aria-label="Listing link"]::attr(href)').extract_first()
            yield response.follow(house_link, callback=self.parse_home)
        next_page = response.css('a[title="Next"]::attr(href)').extract_first()
        if next_page:
            next_page = f'{self.domain}{next_page}'
            yield Request(next_page, callback=self.parse)

    @staticmethod
    def parse_home(response):
        data = dict()
        data['title'] = response.css('h1._64bb5b3b::text').extract_first()
        data['location'] = response.css('div[aria-label="Property header"]::text').extract_first()
        data['beds'] = response.css('span[aria-label="Beds"]::text').extract_first()
        data['baths'] = response.css('span[aria-label="Baths"]::text').extract_first()
        data['area'] = response.css('span[aria-label="Area"]>span::text').extract_first()
        data['property_type'] = response.css('span[aria-label="Type"]::text').extract_first()
        data['price'] = response.css('span[aria-label="Price"]::text').extract_first()
        data['purpose'] = response.css('span[aria-label="Purpose"]::text').extract_first()
        return data
