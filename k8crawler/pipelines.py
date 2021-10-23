# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from k8crawler import settings
import scrapy
import sqlite3

# 値のバリデーションチェック
class ValidationPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if item['year'] is None:
            raise scrapy.exceptions.DropItem('Missing value: title')

        if item['month'] is None:
            raise scrapy.exceptions.DropItem('Missing value: month')

        if item['dates'] is None:
            raise scrapy.exceptions.DropItem('Missing value: dates')

        return item

# sqliteへの保存
class SqlitePipeline(object):
    def open_spider(self, spider: scrapy.Spider):
        # コネクションの開始
        self.conn = sqlite3.connect(settings.SQLITE_PATH)

    def close_spider(self, spider: scrapy.Spider):
        # コネクションの終了
        self.conn.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        sql = "INSERT INTO race_date (date, year, month) VALUES (?, ?, ?)"

        # データの作成
        insert_data_list = []
        for date in item['dates']:
            insert_data_list.append((date, item['year'], item['month']))

        # sqliteへインサート
        curs = self.conn.cursor()
        curs.executemany(sql, insert_data_list)
        self.conn.commit()

        return item