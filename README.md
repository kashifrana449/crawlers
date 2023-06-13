# crawlers
This projects contains scraper for different websites. It is developed using scrapy framework. Pipelines for csv writer
and storing data into relational database has been developed. In this project, Sqlalchemy has been used as ORM.

### Setup:

- we have to download latest chrome driver for selenium. place chrome driver at root directory level along side of settings.py file
- create virtual environment with python==3.6 using annaconda and virtual env. i.e conda create -n crawler python==3.6 and activate virtual env i.e conda activate crawler
- Install requirements.txt file i.e pip install -r requirements.txt
- run `cp config-sample.json config.json` at root level. 
