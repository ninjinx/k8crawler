from k8crawler import settings, const
import scrapy
import pymysql
import re

from k8crawler import items

# レース開催一覧ページのベースURL
NET_KEIBA_URL_BASE = "https://race.netkeiba.com/top/"
RACE_LIST_URL_BASE = NET_KEIBA_URL_BASE + "race_list_sub.html?"
HORSE_URL_BASE = "https://db.netkeiba.com/horse/"


class NetkeibaRaceHistorySpider(scrapy.Spider):
    name = 'netkeiba_race_history'
    allowed_domains = ['race.netkeiba.com', 'db.netkeiba.com']

    def __init__(self, page_limit=3):
        self.page_limit = page_limit
        self.con = pymysql.connect(host=settings.MYSQL_HOST,
                                   user=settings.MYSQL_USER,
                                   password=settings.MYSQL_PASS,
                                   database=settings.MYSQL_DATABASE,
                                   cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.con.close

    def get_race_date(self):
        # 保存済みレコードから未取得のものを取得
        sql = "SELECT date FROM race_date where is_get = 0 limit 1"
        with self.con.cursor() as cursor:
            cursor.execute(sql)
            record = cursor.fetchone()
            if record:
                return record['date']
            return None

    def exists_horse(self, horse_id):
        # 保存済みレコードから未取得のものを取得
        sql = 'SELECT horse_id FROM race_horse_info where horse_id = "' + \
            str(horse_id) + '" limit 1'
        with self.con.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone() != None

    def complete_race_date(self, date):
        # レース日程の完了済みフラグを更新
        sql = 'UPDATE race_date SET is_get = 1 where date = %s and is_get = 0'
        with self.con.cursor() as cursor:
            cursor.execute(sql, date)

        # コミット
        self.con.commit()

    def start_requests(self):
        # 特定のレース日程の結果を取得
        page_num = 0
        while page_num < int(self.page_limit):
            # 未取得データの取得
            race_date = self.get_race_date()

            # 対象の日付が取得できなければ終了
            if not race_date:
                return

            # リクエストを飛ばす
            url = RACE_LIST_URL_BASE + "kaisai_date=" + \
                str(race_date) + "&current_group=" + str(race_date)
            request = scrapy.Request(url, self.parse_race_list)
            request.meta['date'] = race_date
            yield request

            # 確認済みフラグを立てる
            self.logger.info('complete (race_date=' + str(race_date) + ')')
            self.complete_race_date(race_date)

            # ページ数のチェック
            page_num += 1

    def parse_race_list(self, response):
        # 各レースのURL一覧取得
        race_url_list = response.css(
            'li[class*="RaceList_DataItem"]').css('a::attr(href)').getall()
        for race_url in race_url_list:
            if not 'movie' in race_url:
                request = scrapy.Request(
                    NET_KEIBA_URL_BASE + race_url, self.parse_race_result)
                request.meta['date'] = response.meta['date']

                # リクエスト開始
                self.logger.info('start request (race_url=' + race_url + ')')
                yield request

    def parse_race_result(self, response):
        # レース情報の作成
        race_info = self.crate_race_info(response)

        # レース結果の作成
        race_result_data_list = []

        # レースリザルトのレコードを取得
        result_table = response.xpath(
            '//table[@id="All_Result_Table"]/tbody/tr')
        for result_record in result_table:
            # データの初期化
            result_data = items.RaceResult()

            # 除外の馬がいればスキップ
            result_record = result_record.xpath('td')
            if re.search(r'\d+', result_record[0].get()) == None:
                continue

            # レースリザルトのカラムを取得
            for i, result_column in enumerate(result_record):
                # 各カラムの値を反映
                self.reflect_result_data(i, result_column, result_data)

            # リザルトデータを配列に追加
            race_result_data_list.append(result_data)

        # レース情報に反映
        race_info['entry_num'] = len(race_result_data_list)
        race_info['race_results'] = race_result_data_list

        # ウマの情報を取得
        for race_result in race_info['race_results']:
            horse_id = race_result['horse_id']
            if not self.exists_horse(horse_id):
                request = scrapy.Request(
                    HORSE_URL_BASE + horse_id, self.parse_race_horse)
                request.meta['horse_id'] = horse_id

                # リクエスト開始
                self.logger.info('start request (horse_id=' + horse_id + ')')
                yield request

        # レース情報の保存
        yield race_info

    def crate_race_info(self, response):
        # レースの情報を取得
        race_num = response.xpath(
            '//span[@class="RaceNum"]/text()').getall()
        race_data_01 = response.xpath(
            '//div[@class="RaceData01"]/descendant::text()').getall()
        race_data_02 = response.xpath(
            '//div[@class="RaceData02"]/span/text()').getall()
        race_name = response.xpath('//div[@class="RaceName"]/text()').getall()
        race_name_span = response.xpath(
            '//div[@class="RaceName"]/span').getall()
        race_name_span = response.xpath(
            '//div[@class="RaceName"]/span').getall()

        # itemの生成
        race_info = items.RaceInfo()

        # レース情報の登録
        race_info['race_name'] = race_name[0].strip()
        race_info['date'] = response.meta['date']
        race_info['race_num'] = re.search(r'\d+', race_num[0].strip()).group()
        race_info['ground'] = const.Ground.search(race_data_01[1])
        race_info['distance'] = re.search(
            r'\d+', race_data_01[1].strip()).group()
        race_info['weather'] = const.Weather.search(race_data_01[2])
        race_info['clockwise'] = const.Clockwise.search(race_data_01[2])
        race_info['side'] = const.Side.search(race_data_01[2])
        race_info['ground_condition'] = const.GroundCondition.search(
            race_data_01[4])
        race_info['track_id'] = const.Track.search(race_data_02[1])
        race_info['age_condition'] = const.AgeCondition.search(race_data_02[3])
        race_info['class_id'] = self.get_class_by_response(
            race_data_02, race_name_span)
        isMareOnly = 0
        if len(race_data_02) >= 6:
            isMareOnly = const.Sex.search(race_data_02[5]) == const.Sex.SEX_MARE
        race_info['mare_only_flag'] = int(isMareOnly)

        # レース情報の返却
        return race_info

    def get_class_by_response(self, race_data_02, race_name_span):
        # G1,2,3,Lの判定（アイコンでのみ判定可能）
        if race_name_span:
            grade_num = int(re.findall(
                r'Icon_GradeType(\d+)', race_name_span[0])[0])
            if grade_num == 1:
                return const.Class.CLASS_G1
            elif grade_num == 2:
                return const.Class.CLASS_G2
            elif grade_num == 3:
                return const.Class.CLASS_G3
            elif grade_num == 15:
                return const.Class.CLASS_LISTED

        # 文字列から判定
        return const.Class.search(race_data_02[4])

    def reflect_result_data(self, index, result_column, result_data):
        if (index == 0):
            result_data['rank'] = result_column.xpath(
                'div/text()').get()
        elif (index == 1):
            result_data['frame_num'] = result_column.xpath(
                'div/text()').get()
        elif (index == 2):
            result_data['horse_num'] = result_column.xpath(
                'div/text()').get()
        elif (index == 3):
            result_data['horse_id'] = result_column.css(
                'a::attr(href)').get().split('/')[-1]
        elif (index == 4):
            sex_age = result_column.xpath('div/span/text()').get()
            result_data['sex'] = const.Sex.search(sex_age)
            result_data['age'] = re.search(r'\d+', sex_age).group()
        elif (index == 5):
            weight = ''.join(result_column.xpath('div/span/text()').get().split('.'))
            if not weight.isdecimal():
                weight = 0
            result_data['weight'] = weight
        elif (index == 6):
            jockey_id = 0
            jockey_url = result_column.css('a::attr(href)').get()
            if jockey_url:
                search_res = re.search(r'\d+', jockey_url)
                if search_res:
                    jockey_id = search_res.group()
            result_data['jockey_id'] = jockey_id
        elif (index == 7):
            min, sec = result_column.xpath('span/text()').get().split(':')
            sec = ''.join(sec.split('.'))
            result_data['time'] = int(min) * 600 + int(sec)
        elif (index == 8):
            pass
        elif (index == 9):
            popularity = 0
            search_res = result_column.xpath('span/text()').get()
            if search_res:
                popularity = search_res
            result_data['popularity'] = popularity
        elif (index == 10):
            odds = 0
            search_res = result_column.xpath('span/text()').get()
            if search_res:
                odds = ''.join(search_res.split('.'))
            result_data['odds'] = odds
        elif (index == 11):
            last_3f = 0
            search_res = result_column.xpath('text()').get().strip()
            if search_res:
                last_3f = ''.join(search_res.split('.')).strip()
            result_data['last_3f'] = last_3f
        elif (index == 12):
            pass
        elif (index == 13):
            result_data['training_center'] = const.TrainingCenter.search(
                result_column.xpath('span/text()').get())
            trainer_id = 0
            search_result = re.search(r'\d+', result_column.css('a::attr(href)').get())
            if search_result:
                trainer_id = search_result.group()
            result_data['trainer_id'] = trainer_id
        elif (index == 14):
            result_data['horse_weight'] = result_column.xpath(
                'text()').get().strip()
            horse_weight_diff = 0
            search_res = result_column.xpath('small/text()').get()
            if search_res:
                horse_weight_diff = search_res[1:-1]
            result_data['horse_weight_diff'] = horse_weight_diff

    def parse_race_horse(self, response):
        # itemの生成
        horse_info = items.HorseInfo()

        # 馬名
        english_name = re.search(
            r'[ -~]+', response.xpath('//div[@class="horse_title"]/h1/text()').get())
        if not english_name is None:
            horse_info['name'] = english_name.group().strip()
        japan_name = re.search(
            r'[\u30A0-\u30FF]+', response.xpath('//div[@class="horse_title"]/h1/text()').get())
        if not japan_name is None:
            horse_info['name'] = japan_name.group()

        # 性別
        horse_info['sex'] = const.Sex.search(response.xpath(
            '//div[@class="horse_title"]/p[@class="txt_01"]/text()').get())

        # horseIdの取得
        horse_info['horse_id'] = response.meta['horse_id']

        # プロフィールの読み込み
        prof_data_list = response.xpath(
            '//div[@class="db_prof_area_02"]/table/tr')

        # プロフィール情報の反映
        for prof_data in prof_data_list:
            self.reflect_horse_data(prof_data, horse_info)

        # 父母情報
        blood_data_list = response.xpath(
            '//table[@class="blood_table"]/tr')
        horse_info['father_id'] = blood_data_list[0].css(
            'a::attr(href)').getall()[0].split('/')[-2]
        horse_info['father_father_id'] = blood_data_list[0].css(
            'a::attr(href)').getall()[1].split('/')[-2]
        horse_info['father_mother_id'] = blood_data_list[1].css(
            'a::attr(href)').get().split('/')[-2]
        horse_info['mother_id'] = blood_data_list[2].css(
            'a::attr(href)').getall()[0].split('/')[-2]
        horse_info['mother_father_id'] = blood_data_list[2].css(
            'a::attr(href)').getall()[1].split('/')[-2]
        horse_info['mother_mother_id'] = blood_data_list[3].css(
            'a::attr(href)').get().split('/')[-2]

        # 競走馬情報の保存
        yield horse_info

    def reflect_horse_data(self, prof_data, horse_info):
        # カラム名を取得
        column_name = prof_data.xpath('th/text()').get()

        if column_name == '生年月日':
            # 生年月日の取得
            birthday_info = re.findall(
                r'\d+', prof_data.xpath('td/text()').get())
            horse_info['birthday'] = '{:0>4}{:0>2}{:0>2}'.format(
                *birthday_info)
        elif column_name == '調教師':
            # 調教師情報
            trainer_id = 0
            trainer_link = prof_data.css('a::attr(href)').get()
            if not trainer_link is None:
                trainer_id = re.search(r'\d+', trainer_link).group()
            horse_info['trainer_id'] = trainer_id
            # トレセン情報
            horse_info['training_center'] = const.TrainingCenter.search(
                prof_data.xpath('td/text()').get())
        elif column_name == '馬主':
            # 馬主情報
            owner_id = 0
            owner_link = prof_data.css('a::attr(href)').get()
            if not owner_link is None:
                owner_id = re.search(r'\d+', owner_link).group()
            horse_info['owner_id'] = owner_id
        elif column_name == '生産者':
            # 生産者情報
            breeder_id = 0
            breeder_link = prof_data.css('a::attr(href)').get()
            if not breeder_link is None:
                breeder_id = re.search(r'\d+', breeder_link).group()
            horse_info['breeder_id'] = breeder_id
        elif column_name == '産地':
            # 生産地情報
            horse_info['home'] = prof_data.xpath('td/text()').get()
