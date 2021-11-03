# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from k8crawler import settings
import scrapy
import pymysql

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
        self.con = pymysql.connect(host=settings.MYSQL_HOST,
                                   user=settings.MYSQL_USER,
                                   password=settings.MYSQL_PASS,
                                   database=settings.MYSQL_DATABASE,
                                   cursorclass=pymysql.cursors.DictCursor)

    def close_spider(self, spider: scrapy.Spider):
        # コネクションの終了
        self.con.close

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        sql = "INSERT INTO race_date (date, year, month) VALUES (%s, %s, %s)"

        # データの作成
        insert_data_list = []
        for date in item['dates']:
            insert_data_list.append((date, item['year'], item['month']))

        # sqliteへインサート
        with self.con.cursor() as cursor:
            cursor.executemany(sql, insert_data_list)

        # コミット
        self.con.commit()

        return item