from scrapy import FormRequest
from copy import deepcopy
from datetime import datetime

from scrapers.spiders.base_spider import BaseSpider


class SheriffMugshots(BaseSpider):
    name = 'Sheriff Mugshots'
    base_url = 'http://etowahsmartweb.kalleo.net'
    api_url = 'http://etowahsmartweb.kalleo.net/smartweb/Jail.aspx/AddMoreResults'
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 300,
    }
    form_data = {
        "FirstName":"","MiddleName":"","LastName":"","BeginBookDate":"1/1/2004","EndBookDate":"","BeginReleaseDate":"",
        "EndReleaseDate":"","TypeJailSearch":"2","RecordsLoaded":50,"SortOption":"0","SortOrder":"0"
    }
    start_record = 0

    def start_request(self):
        form_data = deepcopy(self.form_data)
        form_data['EndBookDate'] = datetime.now().strftime('d/m/Y')
        form_data['RecordsLoaded'] = self.start_record
        yield FormRequest(self.api_url, formdata=form_data, method='POST')

    def parse(self, response):
        print('')
