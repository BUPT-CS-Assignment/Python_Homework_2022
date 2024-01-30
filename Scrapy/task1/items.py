# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseData(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    location = scrapy.Field()
    room = scrapy.Field()
    area = scrapy.Field()
    unit_price = scrapy.Field()
    total_price = scrapy.Field()


class SecHandHouseData(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    type = scrapy.Field()
    unit_price = scrapy.Field()
    total_price = scrapy.Field()