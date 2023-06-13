# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from os import path, makedirs
from csv import DictWriter


from settings import csv_storage


class CSVPipeline(object):
    buffer = list()
    buffer_busy = list()
    buffer_size = 5
    file_path = None
    write_headers = True

    def open_spider(self, spider):
        directory_path = path.join(csv_storage, spider.name)
        makedirs(directory_path, exist_ok=True)
        self.csv_file_name = f'{spider.name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
        self.file_path = path.join(csv_storage, spider.name, self.csv_file_name)

    def close_spider(self, spider):
        if len(self.buffer) > 0:
            self.write_into_csv_file()
            self.buffer.clear()

    def write_into_csv_file(self):
        with open(self.file_path, 'a') as file:
            dict_writer = DictWriter(file, fieldnames=list(self.buffer[0].keys()))
            if self.write_headers:
                dict_writer.writeheader()
                self.write_headers = False
            dict_writer.writerows(self.buffer)

    def process_item(self, item, spider):
        if len(self.buffer) < self.buffer_size:
            self.buffer.append(item)
        else:
            self.write_into_csv_file()
            self.buffer.clear()
            self.buffer.append(item)
        return item
