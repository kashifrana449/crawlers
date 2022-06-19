from scrapy import Request, FormRequest
from datetime import datetime
from json import loads, dumps
from re import findall

from scrapers.models.crime.family_watch_dog import FamilyWatchDogLocation
from scrapers.models.big_data.spy_one import SpyOne
from scrapers.models.big_data.proxy_free_list import FreeProxyList
from scrapers.spiders.base_spider import BaseSpider


class FamilyWatchDogCrimeSpider(BaseSpider):
    name = 'Family Watch Dog Crime'
    base_url = 'https://www.familywatchdog.us/'
    custom_settings = {
        'ROTATING_PROXY_PAGE_RETRY_TIMES': 10,
        'ITEM_PIPELINES': {'scrapers.pipelines.crime.fwd_crime.FWDCrimePipeline': 300},
    }
    use_splash = True
    use_db_proxy = True
    splash_args = {
        'splash': {'wait': 5, 'js_enabled': True, 'args': {'images': 1, 'html5_media': 1, 'timeout': 30, 'http_method': 'POST'}}
    }

    @classmethod
    def read_proxy_list(cls):
        """free proxy list"""
        records = FreeProxyList.query.with_entities(FreeProxyList.proxy)
        cls.proxy_list = [x.proxy for x in records]
        """proxies from SpyOne"""
        # records = SpyOne.query.with_entities(SpyOne.proxy)
        # cls.proxy_list = [x.proxy for x in records]
        """proxies from FREE PROXY"""
        # records = FreeProxy.query.with_entities(FreeProxy.ip, FreeProxy.port)
        # cls.proxy_list = [f"{x.ip}:{x.port}" for x in records]

    def start_requests(self):
        link = 'https://www.familywatchdog.us/showmap.asp'
        locations = FamilyWatchDogLocation.query.filter(FamilyWatchDogLocation.bbox != 'null',
                                                        FamilyWatchDogLocation.center != 'null',
                                                        FamilyWatchDogLocation.id <= 10000,
                                                        ).all()
        for location in locations:
            center = loads(location.center)
            form_data = {'txtStreet1': location.location, 'txtStreet2': '', 'txtCity': '', 'txtState': '',
                         'txtBrowser': '', 'txtZipCode': '', 'txtLatitude': str(center[1]), 'txtLongitude': str(center[0]),
                         'txtCLatitude': str(center[1]), 'txtCLongitude': str(center[0]), 'txtGeoCity': '',
                         'txtGeoState': '', 'SKID': '', 'Message': '', 'XML': ''
                         }
            yield FormRequest(url=link, formdata=form_data, meta={'bbox': location.bbox, 'location': location.location,
                                                                  'center': dumps(center)}, callback=self.parse)

    def parse(self, response):
        bbox = loads(response.meta.get('bbox'))
        swl = bbox[1]
        swln = bbox[0]
        nel = bbox[3]
        neln = bbox[2]
        response.meta['txtLatitude'] = response.css('#txtLatitude::attr(value)').extract_first('')
        response.meta['txtLongitude'] = response.css('#txtLongitude::attr(value)').extract_first('')
        search_id = ''.join(findall("guid = '(.+)", response.text)).strip().replace("\';", '')
        if search_id and ((swl or swln) and (nel or neln)):
            link = (f"https://www.familywatchdog.us/mapmarkers.asp?ndm=0&lat={swl}&lon={swln}&swLat={swl}&swLon={swln}"
                    f"&neLat={nel}&neLon={neln}&searchid={search_id}")
            yield Request(link, callback=self.parse_crime, meta=response.meta)

    def parse_crime(self, response):
        location = response.meta.get('location')
        bbox = loads(response.meta.get('bbox'))
        center = loads(response.meta.get('center'))
        try:
            crimes = loads(response.text)
        except Exception as e:
            print(e)
            return
        for crime in crimes.get('markers', []):
            item = dict()
            item['oid'] = crime.get('oid')
            item['aid'] = crime.get('aid')
            item['latitude'] = crime.get('lt')
            item['longitude'] = crime.get('ln')
            item['c'] = crime.get('c')
            item['mt'] = crime.get('mt')
            item['at'] = crime.get('at')
            response.meta['item'] = item
            form_data = {
                'txtStreet1': location, 'txtCity': '', 'txtState': '', 'txtZipCode': '',
                'txtLatitude': str(response.meta['txtLatitude']), 'txtLongitude': str(response.meta['txtLongitude']),
                'txtCLatitude': str(center[1]), 'txtCLongitude': str(center[0]), 'txtGeoCity': '',
                'txtGeoState': '', 'Message': '', 'txtZoomLevel': '12.5', 'oid': str(item['oid']),
                'rm': 'undefined', 'rp': '1', 'vi': '', 'ndm': '0', 'swl': str(bbox[1]), 'swln': str(bbox[0]),
                'nel': str(bbox[3]), 'neln': str(bbox[2]), 'numdays': '0',
            }
            if crime['oid'] != 'XXX' and crime['at'] != 'sc':
                link = 'https://www.familywatchdog.us/ViewOffender.asp'
                yield FormRequest(link, formdata=form_data, meta=response.meta, callback=self.parse_offender)

    def parse_offender(self, response):
        response_item = response.meta.get('item', {})
        keys = [x.replace(':', '').replace('(s)', '').strip() for x in
                response.css('.offender-details-center-two strong::text').extract()]
        risk_text = response.css('.offender-details-center-two em>div::text').extract()
        values = [''.join(x.css('::text').extract()) for x in response.css('.offender-details-center-two em') if
                  risk_text not in x.css('::text').extract()]
        risk_text = self.get_index([''.join(x.css(' ::text').extract())
                                    for x in response.css('.offender-details-center-two em')
                                    if risk_text in x.css(' ::text').extract()], 0)
        state = response.css('.offender-details-center-two>div ::text').extract_first()
        data = dict(zip(keys, values))
        try:
            if ',' in data.get('DOB', ''):
                data['DOB'] = self.get_index(data['DOB'].split(','), 0)
                data['Age'] = self.get_index(data['Age'].split(','), 0)
            if '/' in data.get('DOB', ''):
                data['DOB'] = datetime.strptime(data.get('DOB'), '%m/%d/%Y').date() if data.get('DOB') else ''
            elif '-' in data.get('DOB', ''):
                data['DOB'] = datetime.strptime(data.get('DOB'), '%m-%d-%Y').date() if data.get('DOB') else ''
        except Exception as e:
            print('date of birth ', data.get('DOB', ''))
            print(e.args)
        if state and len(state.split(':')) == 2:
            state = state.split(':')
            data[state[0]] = state[1]
        if risk_text and len(risk_text.split(':')) == 2:
            risk_text = risk_text.split(':')
            data[risk_text[0]] = risk_text[1]
        item = {
            'name': data.get('Name', ''),
            'DOB': data.get('DOB'),
            'age': data.get('Age', 0),
            'sex': data.get('Sex', ''),
            'race': data.get('Race', ''),
            'height': data.get('Height', ''),
            'weight': data.get('Weight', ''),
            'hair': data.get('Hair', ''),
            'eye': data.get('Eye', ''),
            'homeAddress': data.get('Home Address'),
            'latitude': self.get_index(loads(response.meta.get('center', [])), 1),
            'longitude': self.get_index(loads(response.meta.get('center', [])), 0),
            'registeredState': data.get('Registering State'),
            'aid': response_item.get('aid'),
            'oid': response_item.get('oid'),
            'c': response_item.get('c'),
            'mt': response_item.get('mt'),
            'at': response_item.get('at'),
            'school': '',
        }
        crime_detail = []
        for crime_date, crime_desc in zip(response.css('#con3 strong::text').extract(),
                                          response.css('#con3 em::text').extract()):
            c_item = dict()
            c_item['crimeDate'] = crime_date
            c_item['crimeDescription'] = crime_desc
            crime_detail.append(c_item)
        item['crimeDetail'] = crime_detail
        crimes_records = []
        for record in response.css('.offender-report2:not(.header)'):
            data = dict()
            data['name'] = record.css('.name a::text').extract_first()
            data['age'] = record.css('.age::text').extract_first()
            data['location'] = record.css('.location ::text').extract_first()
            crimes_records.append(data)
        item['totalCrimes'] = len(crimes_records)
        item['crimes'] = crimes_records

        if item.get('name'):
            yield item
