# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RentingItem(scrapy.Item):
    id = scrapy.Field()         # 标号
    name = scrapy.Field()       # 名称
    city = scrapy.Field()       # 城市
    cbd = scrapy.Field()        # 板块
    ad_code = scrapy.Field()    # 广告标识
    brand = scrapy.Field()      # 房源品牌
    price = scrapy.Field()      # 总价
    addition = scrapy.Field()   # 附加信息(面积、户型、朝向)
    
    
    
class CBDItem(scrapy.Item):
    city = scrapy.Field()       # 城市
    region = scrapy.Field()     # 地区
    name = scrapy.Field()       # 名称
    url = scrapy.Field()        # 链接
    total = scrapy.Field()      # 总租房数
    pages = scrapy.Field()      # 总页数
    