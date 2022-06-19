from selenium import webdriver
from os.path import join
from random import choice

from scrapers.spiders.base_spider import BaseSpider
from scrapers.models.big_data.proxy_free_list import FreeProxyList
from settings import PROJECT_DIRECTORY


class LinkedInJobs(BaseSpider):
    title = 'LinkedIn Users'
    name = 'linkedin_users'
    base_url = 'https://www.linkedin.com/'
    proxies = []
    drivers = []
    error_list = [
        'ERR_PROXY_CONNECTION_FAILED', 'ERR_TUNNEL_CONNECTION_FAILED', 'ERR_TIMED_OUT'
        ''
    ]
    accounts = {
        'account1': {'username': 'masthababa12345@gmail.com', 'password': 'fakebaba938'},
        'account2': {'username': 'masthababa12346@gmail.com', 'password': 'fakebaba939'},
        'account3': {'username': 'masthababa12347@gmail.com', 'password': 'fakebaba940'}
    }

    def create_driver(self):
        proxy = self.proxies.pop()
        desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        desired_capabilities['proxy'] = {
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False
        }
        driver = webdriver.Chrome(executable_path=join(PROJECT_DIRECTORY, 'chromedriver'),
                                  desired_capabilities=desired_capabilities)
        # driver = webdriver.Chrome(executable_path=join(PROJECT_DIRECTORY, 'chromedriver'))
        return driver

    def initialize_driver(self):
        page = 'ERR_PROXY_CONNECTION_FAILED'
        driver = None
        while any(a in page for a in self.error_list):
            driver = self.create_driver()
            driver.get('https://www.linkedin.com/login')
            page = driver.page_source
            if any(a in page for a in self.error_list):
                driver.close()
                driver.quit()
                del driver
        return driver

    def start_requests(self):
        self.proxies = [x for x, in FreeProxyList.query.with_entities(FreeProxyList.proxy).all()]
        for i in range(0, 10):
            driver = self.initialize_driver()
            account = choice(list(self.accounts.keys()))
            driver.find_element_by_id('username').send_keys(self.accounts[account]['username'])
            driver.find_element_by_id('password').send_keys(self.accounts[account]['password'])
            driver.find_element_by_class_name('login__form_action_container ').click()
            print('')
            self.drivers.append(driver)


    def parse(self, response):
        print('')
