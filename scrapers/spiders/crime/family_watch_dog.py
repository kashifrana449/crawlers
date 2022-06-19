from scrapy import Spider, Request
from json import loads, dumps, JSONDecodeError
from re import findall

from scrapers.models.country_stats import UsCities


class FamilyWatchDogLocationSpider(Spider):
    name = 'Family Watch Dog'
    base_url = 'https://www.familywatchdog.us/'
    custom_settings = {
        'ITEM_PIPELINES': {'scrapers.pipelines.crime.fwd_location.FWDLocationPipeline': 300},
    }

    def start_requests(self):
        yield Request(self.base_url)

    def parse(self, response):
        access_token = ''.join(findall(r'mapboxgl.accessToken =(.+);', response.text)).replace('\'', '').strip()
        if access_token:
            cities = UsCities.query.with_entities(UsCities.cityName.distinct())
            for city in cities:
                link = (f'https://api.mapbox.com/geocoding/v5/mapbox.places/{city[0]}.json?access_token='
                        f'{access_token}&proximity=74.344%2C31.55&country=us&limit=5')
                yield Request(link, callback=self.parse_location)

    def parse_location(self, response):
        try:
            json_response = loads(response.text)
        except JSONDecodeError as e:
            print(e)
            return
        for data in json_response.get('features'):
            item = dict()
            item['location'] = data.get('place_name')
            item['bbox'] = dumps(data.get('bbox'))
            item['center'] = dumps(data.get('center'))
            yield item
