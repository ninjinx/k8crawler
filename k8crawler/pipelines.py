# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from k8crawler import items, settings
import scrapy
import pymysql


# 値のバリデーションチェック
class ValidationPipeline(object):
    def process_item(self, item, spider):
        # アイテムの取得
        adapter = ItemAdapter(item)

        # アイテムごとに処理を振り分け
        if isinstance(item, items.raceDate):
            self.validate_race_date(adapter)
        elif isinstance(item, items.HorseInfo):
            self.validate_horse_info(adapter)
        elif isinstance(item, items.RaceInfo):
            self.validate_race_info(adapter)
        else:
            raise scrapy.exceptions.DropItem('unsupported item')

        return item

    def validate_race_date(self, adapter):
        for column in items.raceDate.fields.keys():
            if adapter[column] is None:
                raise scrapy.exceptions.DropItem('Missing value: ' + column)

    def validate_horse_info(self, adapter):
        for column in items.HorseInfo.fields.keys():
            if adapter[column] is None:
                raise scrapy.exceptions.DropItem('Missing value: ' + column)

    def validate_race_info(self, adapter):
        # レース情報のバリデーション
        for column in items.RaceInfo.fields.keys():
            if adapter[column] is None:
                raise scrapy.exceptions.DropItem('Missing value: ' + column)

        # レース結果のバリデーション
        for race_result in adapter['race_results']:
            for column in items.RaceResult.fields.keys():
                if race_result[column] is None:
                    raise scrapy.exceptions.DropItem(
                        'Missing value: ' + column)


# mysqlへの保存
class MysqlPipeline(object):
    def open_spider(self, spider):
        # コネクションの開始
        self.con = pymysql.connect(host=settings.MYSQL_HOST,
                                   user=settings.MYSQL_USER,
                                   password=settings.MYSQL_PASS,
                                   database=settings.MYSQL_DATABASE,
                                   cursorclass=pymysql.cursors.DictCursor)

    def close_spider(self, spider):
        # コネクションの終了
        self.con.close

    def process_item(self, item, spider):
        # アイテムの取得
        adapter = ItemAdapter(item)

        # アイテムごとに処理を振り分け
        if isinstance(item, items.raceDate):
            self.save_race_date(adapter)
        elif isinstance(item, items.HorseInfo):
            self.save_horse_info(adapter)
        elif isinstance(item, items.RaceInfo):
            self.save_race_info(adapter)
        else:
            raise scrapy.exceptions.DropItem('unsupported item')

        return item

    def save_race_date(self, adapter):
        # クエリの作成
        sql = "INSERT INTO race_date (date, year, month) VALUES (%s, %s, %s)"

        # データの作成
        insert_data_list = []
        for date in adapter['dates']:
            insert_data_list.append((date, adapter['year'], adapter['month']))

        # mysqlへインサート
        with self.con.cursor() as cursor:
            cursor.executemany(sql, insert_data_list)

        # コミット
        self.con.commit()

    def save_horse_info(self, adapter):
        # save
        keys = []
        values = []
        for k, v in adapter.items():
            keys.append(k)
            values.append(str(v))

        # クエリの作成
        sql = 'INSERT INTO race_horse_info (' + ', '.join(
            keys) + ') VALUES (' + ', '.join(['%s' for _ in keys]) + ')'

        # mysqlへインサート
        with self.con.cursor() as cursor:
            cursor.execute(sql, values)

        # コミット
        self.con.commit()

    def save_race_info(self, adapter):
        # レースIDの生成
        race_id = '{:0>8}{:0>2}{:0>2}'.format(
            adapter['date'], adapter['track_id'], adapter['race_num'])

        # レース情報の作成
        race_info_keys = ['race_id']
        race_info_values = [race_id]
        for k, v in adapter.items():
            if k == 'race_results':
                race_results = adapter['race_results']
                continue
            race_info_keys.append(k)
            race_info_values.append(str(v))

        # レース情報クエリの作成
        race_info_sql = 'INSERT INTO race_info (' + ', '.join(
            race_info_keys) + ') VALUES (' + ', '.join(['%s' for _ in race_info_keys]) + ')'

        # レース結果情報の作成
        race_result_values = []
        race_result_keys = ['race_id'] + list(items.RaceResult.fields.keys())
        for race_result in race_results:
            race_result_value = []

            # キーの順序に従い値を取得
            for k in race_result_keys:
                if k == 'race_id':
                    race_result_value.append(str(race_id))
                    continue
                race_result_value.append(str(race_result[k]))

            # 結果の格納
            race_result_values.append(race_result_value)

        # レースリザルトクエリの作成
        race_result_sql = 'INSERT INTO race_horse_result (' + ', '.join(
            race_result_keys) + ') VALUES (' + ', '.join(['%s' for _ in race_result_keys]) + ')'

        # mysqlへインサート
        race_info_exist_sql = 'SELECT race_id FROM race_info where race_id = %s limit 1'
        race_result_exist_sql = 'SELECT race_id FROM race_horse_result where race_id = %s limit 1'
        with self.con.cursor() as cursor:
            # レース情報のインサート処理
            cursor.execute(race_info_exist_sql, race_id)
            if not cursor.fetchone():
                cursor.execute(race_info_sql, race_info_values)

            # レース結果のインサート処理
            cursor.execute(race_result_exist_sql, race_id)
            if not cursor.fetchone():
                cursor.executemany(race_result_sql, race_result_values)

        # コミット
        self.con.commit()
