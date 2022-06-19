from json import loads
from os import getcwd
from os.path import expanduser

with open(expanduser('./config.json')) as config_file:
    config = loads(config_file.read())

# -*- coding: utf-8 -*-

# Scrapy settings for BigData project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

MYSQL_DB_CREDENTIALS = config['MYSQL_DB_CREDENTIALS']

MYSQL_DB_SPORTS = dict(MYSQL_DB_CREDENTIALS, db="sports")
MYSQL_DB_REAL_ESTATE = dict(MYSQL_DB_CREDENTIALS, db='real_estate')
MYSQL_DB_COUNTRY_STATS = dict(MYSQL_DB_CREDENTIALS, db='country_stats')
MYSQL_DB_BIG_DATA = dict(MYSQL_DB_CREDENTIALS, db='big_data')
MYSQL_DB_CRIME = dict(MYSQL_DB_CREDENTIALS, db='crime')
MYSQL_DB_URI = config['MYSQL_DB_URI']


BOT_NAME = 'BigData'
DEBUG = True
PROJECT_DIRECTORY = f"{getcwd().split('BigData')[0]}/BigData/BigData/"
# SPIDER_MODULES = ['scrapers.spiders']
# NEWSPIDER_MODULE = 'scrapers.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENTS = [
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/76.0.3809.132 Safari/537.36'),
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    ('Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) '
     'Version/4.0 Safari/534.30'),
]

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1
RETRY_TIMES = 3
ROTATING_PROXY_PAGE_RETRY_TIMES = 15

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
TIMEOUT_EXPRESSION = '(%s)*24*360'
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'BigData.middlewares.BigdataSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    # 'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
    # 'BigData.middlewares.BigdataDownloaderMiddleware': 543,
}

SPLASH_URL = 'http://localhost:8050/'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'BigData.pipelines.BigdataPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
RETRY_HTTP_CODES = [500, 501, 502, 503, 504, 400, 403, 404, 408, 302, 300]
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
