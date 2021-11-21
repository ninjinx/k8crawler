# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class raceDate(scrapy.Item):
    year = scrapy.Field()
    month = scrapy.Field()
    dates = scrapy.Field()


class RaceInfo(scrapy.Item):
    race_name = scrapy.Field()
    date = scrapy.Field()
    track_id = scrapy.Field()
    race_num = scrapy.Field()
    distance = scrapy.Field()
    clockwise = scrapy.Field()
    side = scrapy.Field()
    ground = scrapy.Field()
    ground_condition = scrapy.Field()
    weather = scrapy.Field()
    mare_only_flag = scrapy.Field()
    age_condition = scrapy.Field()
    class_id = scrapy.Field()
    entry_num = scrapy.Field()
    race_results = scrapy.Field()


class RaceResult(scrapy.Item):
    age = scrapy.Field()
    frame_num = scrapy.Field()
    horse_id = scrapy.Field()
    horse_num = scrapy.Field()
    horse_weight = scrapy.Field()
    horse_weight_diff = scrapy.Field()
    jockey_id = scrapy.Field()
    last_3f = scrapy.Field()
    odds = scrapy.Field()
    popularity = scrapy.Field()
    rank = scrapy.Field()
    sex = scrapy.Field()
    time = scrapy.Field()
    trainer_id = scrapy.Field()
    training_center = scrapy.Field()
    weight = scrapy.Field()


class HorseInfo(scrapy.Item):
    horse_id = scrapy.Field()
    name = scrapy.Field()
    birthday = scrapy.Field()
    sex = scrapy.Field()
    home = scrapy.Field()
    breeder_id = scrapy.Field()
    owner_id = scrapy.Field()
    training_center = scrapy.Field()
    trainer_id = scrapy.Field()
    father_id = scrapy.Field()
    mother_id = scrapy.Field()
