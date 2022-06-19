from scrapy import Spider, signals
from datetime import datetime

import settings
from scrapers.models.big_data.free_proxy import FreeProxy


class BaseSpider(Spider):

    new_settings = {}
    use_db_proxy = False
    use_splash = False
    proxy_list = []
    frequency = 1
    error_threshold = 1000

    @classmethod
    def read_proxy_list(cls):
        if hasattr(cls, 'use_db_proxy') and cls.use_db_proxy:
            cls.proxy_list = list(map(lambda x: f'{x.https}://{x.ip}:{x.port}', FreeProxy.
                                      query.with_entities(FreeProxy.ip, FreeProxy.port, FreeProxy.https
                                                          ).filter(FreeProxy.https == 'http').all()))

    @classmethod
    def update_settings(cls, _settings):
        cls.new_settings['DOWNLOADER_MIDDLEWARES'] = {**settings.DOWNLOADER_MIDDLEWARES}
        cls.new_settings['CLOSESPIDER_ERRORCOUNT'] = cls.error_threshold
        # cls.new_settings['CLOSESPIDER_TIMEOUT'] = eval(settings.TIMEOUT_EXPRESSION % str(cls.frequency))
        if hasattr(cls, 'use_db_proxy') and cls.use_db_proxy:
            cls.new_settings['PROXY_MODE'] = 0
            cls.new_settings['DOWNLOADER_MIDDLEWARES'].update({
                # 'scrapy_proxies.RandomProxy': 100,
                'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
                'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
            })
            cls.read_proxy_list()
            cls.new_settings['ROTATING_PROXY_LIST'] = cls.proxy_list
            # cls.new_settings['PROXY_LIST'] = list(map(lambda x: f'{x.https}://{x.ip}:{x.port}', FreeProxy.
            #                                           query.with_entities(FreeProxy.ip, FreeProxy.port,
            #                                                               FreeProxy.https).all()))
            cls.new_settings['proxy_enable'] = True
        if hasattr(cls, 'use_splash') and cls.use_splash:
            cls.new_settings['DOWNLOADER_MIDDLEWARES'].update({
                # 'scrapy_splash.SplashCookiesMiddleware': 723,
                'scrapy_splash.SplashMiddleware': 725,
                'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
            })
            _settings.setdict(cls.new_settings, priority='spider')
            # cls.new_settings['SPIDER_MIDDLEWARES'] = {
            #     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
            # }
        if hasattr(cls, 'custom_settings') and cls.custom_settings:
            cls.new_settings.update(cls.custom_settings)
        _settings.setdict(cls.new_settings, priority='spider')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.open_spider, signal=signals.spider_opened)
        crawler.signals.connect(spider.close_spider, signal=signals.spider_closed)
        return spider

    def open_spider(self, spider):
        scraper_stats = dict()
        scraper_stats['name'] = getattr(spider, 'name')
        scraper_stats['startTime'] = datetime.now()
        scraper_stats['frequency'] = spider.frequency

    def close_spider(self, spider):
        pass

    @staticmethod
    def get_index(data, index, default=''):
        if index >= 0 and data:
            return data[index] if len(data) > index else default
        elif data:
            return data[index] if len(data) >= abs(index) else default
        else:
            return default
