from k8crawler import settings
from ..items import raceDate
import scrapy
import datetime
import sqlite3
import re

# レース開催一覧ページのベースURL
RACE_DATE_URL_BASE = "https://race.netkeiba.com/top/calendar.html?"
# 開催年月初期値
INIT_YEAR = 2008
INIT_MONTH = 1

class NetkeibaRaceDateSpider(scrapy.Spider):
    name = 'netkeiba_race_date'
    allowed_domains = ['www.netkeiba.com/']

    def __init__(self, page_limit=3):
        self.page_limit = page_limit
        self.con = sqlite3.connect(settings.SQLITE_PATH)

    def __del__(self):
        self.con.close

    def add_month(self, year, month, add):
        # 月に加算
        month += add

        # 繰り上げ処理
        while month > 12:
            year += 1
            month -= 12

        return year, month

    def get_init_date(self):
        # 保存済みレコードから最新のものを取得
        sql = "SELECT year, month FROM race_date order by date DESC limit 1"
        race_date_max = self.con.execute(sql).fetchone()

        # 初期値の取得
        init_year = INIT_YEAR
        init_month = INIT_MONTH

        # レコードが存在すれば次月から取得
        if race_date_max:
            init_year, init_month = self.add_month(race_date_max[0], race_date_max[1], 1)

        return init_year, init_month

    def start_requests(self):
        # 現在の年月日を取得
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

        # 保存済みレコードの最新値取得
        year, month = self.get_init_date()

        # 現時点（先月）までのレース一覧を取得
        page_num = 0
        while page_num < int(self.page_limit):
            # 現在時点に達していたら終了
            if year >= now.year and month >= now.month:
                return

            # リクエストを飛ばす
            yield scrapy.Request(RACE_DATE_URL_BASE + "year=" + str(year) + "&month=" + str(month))

            # ページ数のチェック
            page_num += 1

            # 月の加算
            year, month = self.add_month(year, month, 1)


    def parse(self, response):
        # 年月を取得
        nums = re.findall(r'\d+', response.url)
        year = nums[0]
        month = nums[1]

        # レース開催日のリスト取得
        raceKaisaiBoxes = response.css("div.RaceKaisaiBox")

        # レース開催している日付を取得
        race_dates = []
        for box in raceKaisaiBoxes:
            if box.css("span.JyoName::text").getall():
                day = box.css("span.Day::text").get()
                race_dates.append('{:0>4}{:0>2}{:0>2}'.format(year, month, day))

        # レース日の返却
        yield raceDate(year=year, month=month, dates=race_dates)