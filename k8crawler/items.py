# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class raceDate(scrapy.Item):
    year = scrapy.Field()
    month = scrapy.Field()
    dates = scrapy.Field()
