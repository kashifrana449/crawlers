from scrapy import Request
from json import loads, dumps, JSONDecodeError

from scrapers.spiders.base_spider import BaseSpider
from constants import CATEGORY
from scrapers.models.big_data.proxy_free_list import FreeProxyList


class ReNzSpider(BaseSpider):
    name = 'RealEstate NZ'
    category = CATEGORY['REAL_ESTATE']
    frequency = 7
    use_db_proxy = True
    base_url = 'https://www.realestate.co.nz/'

    custom_settings = {
        'ITEM_PIPELINES': {'scrapers.pipelines.real_estate.re_nz.re_nz.ReNzPipeline': 300},
    }

    url = ('https://platform.realestate.co.nz/search/v1/listings?filter%5Bcategory%5D%5B0%5D='
           'res_sale&page%5BgroupBy%5D=featured&page%5Blimit%5D={}&page%5Boffset%5D={}')

    @classmethod
    def read_proxy_list(cls):
        if hasattr(cls, 'use_db_proxy') and cls.use_db_proxy:
            cls.proxy_list = [x for x, in FreeProxyList.query.with_entities(FreeProxyList.proxy).all()]

    def start_requests(self):
        offset = 0
        limit = 20
        link = self.url.format(limit, offset)
        yield Request(link, meta={'offset': offset, 'limit': limit, 'max_proxies_to_try': 40})

    def parse(self, response):
        offset = response.meta.get('offset')
        offset += 1
        limit = response.meta.get('limit')
        limit += 1
        try:
            response_json = loads(response.text)
        except JSONDecodeError as e:
            print(e)
            return
        except Exception as e:
            print(e)
            return
        included_info = response_json.get('included')
        for property_item in response_json.get('data'):
            item = dict()
            item['propertyId'] = property_item.get('id')
            attributes = property_item.get('attributes')
            item['price'] = attributes.get('price-display')
            item['area'] = attributes.get('land-area')
            item['category'] = attributes.get('listing-category-code')
            item['parkingOtherCount'] = str(attributes.get('parking-other-count'))
            item['publishedDate'] = attributes.get('published-date')
            item['bed'] = str(attributes.get('bedroom-count'))
            item['listingId'] = attributes.get('listing-no')
            item['areaUnit'] = attributes.get('land-area-unit')
            item['propertyCreatedDate'] = attributes.get('created-date')
            item['parkingGarageCount'] = str(attributes.get('parking-garage-count', ''))
            item['storyCount'] = str(attributes.get('storey-count', ''))
            item['maxTenants'] = str(attributes.get('max-tenants'))
            item['floorArea'] = attributes.get('floor-area')
            item['bathCount'] = str(attributes.get('bathroom-full-count', ''))
            item['bathEnsuiteCount'] = str(attributes.get('bathroom-ensuite-count', ''))
            item['bathWcCount'] = str(attributes.get('bathroom-wc-count', ''))
            item['hasSwimmingPool'] = str(attributes.get('has-swimming-pool', ''))
            item['propertyType'] = attributes.get('listing-sub-type')
            item['listingStatus'] = attributes.get('listing-status')
            open_homes = attributes.get('open-homes')
            if open_homes:
                openings = []
                for open_home in open_homes:
                    time = dict()
                    time['id'] = open_home.get('id')
                    time['start'] = open_home.get('start')
                    time['end'] = open_home.get('end')
                    openings.append(time)
                item['openHomes'] = dumps(openings)
            address = attributes.get('address')
            if address:
                item['country'] = address.get('country')
                item['region'] = address.get('region')
                item['district'] = address.get('district')
                item['subUrb'] = address.get('suburb')
                item['latitude'] = address.get('latitude')
                item['longitude'] = address.get('longitude')
                item['streetNumber'] = address.get('street-number')
                item['street'] = address.get('street')
                item['postCode'] = address.get('postcode')
                item['address'] = address.get('address') or address.get('full-address')
                item['nearBySuburb'] = dumps(address.get('nearby-suburbs'))
                item['nearbySuburbSlugs'] = dumps(attributes.get('nearby-suburbs-fq-slugs'))
            additional_website = attributes.get('additional-websites')
            item['additionalWebsites'] = None
            if additional_website:
                urls = [uri.get('url') for uri in additional_website]
                item['additionalWebsites'] = dumps(urls)
            schools = property_item.get('schools')
            item['schools'] = None
            if schools:
                school_list = []
                for school in schools:
                    sc = dict()
                    sc['schoolId'] = school.get('bathroom-wc-count')
                    sc['geoRadius'] = school.get('geo-radius')
                    sc['inZone'] = school.get('in-zone')
                    sc['name'] = school.get('organization-name')
                    sc['latitude'] = self.get_index(school.get('geo-point', []), 1)
                    sc['longitude'] = self.get_index(school.get('geo-point'), [], 0)
                    school_list.append(sc)
                item['schools'] = dumps(school_list)
            relationships = property_item.get('relationships')
            if relationships:
                offices = relationships.get('offices')
                item['offices'] = None
                if offices:
                    offices_id_list = [x.get('id') for x in offices.get('data')]
                    included_offices = list(filter(lambda data: (data.get('id') in offices_id_list) and (
                            data.get('type') == 'office'), included_info))
                    offices_list = list()
                    for office in included_offices:
                        office_item = dict()
                        attribute = office.get('attributes')
                        office_item['officeId'] = office.get('id')
                        office_item['officeName'] = attribute.get('name')
                        offices_list.append(office_item)
                    item['offices'] = dumps(offices_list)
                agents = relationships.get('agents')
                item['agents'] = None
                if agents:
                    agents_id_list = [x.get('id') for x in agents.get('data')]
                    included_agents = list(filter(lambda data: (data.get('id') in agents_id_list) and (
                            data.get('type') == 'agent'), included_info))
                    agents_list = list()
                    for agent in included_agents:
                        agent_item = dict()
                        attribute = agent.get('attributes')
                        agent_item['id'] = agent.get('id')
                        agent_item['name'] = attribute.get('name')
                        agent_item['phone'] = attribute.get('phone-mobile')
                        agents_list.append(agent_item)
                    item['agents'] = dumps(agents_list)
            yield item
        link = self.url.format(limit, offset)
        yield Request(link, meta={'offset': offset, 'limit': limit, 'max_proxies_to_try': 40})
