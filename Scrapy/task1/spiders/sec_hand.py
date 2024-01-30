import scrapy
from scrapy import Request
from task1.items import *
from bs4 import BeautifulSoup


class SecHandHouseSpider(scrapy.Spider):
    name = 'sec_hand'
    allowed_domains = ['bj.fang.lianjia.com']
    custom_settings = {
        'ITEM_PIPELINES':{'task1.pipelines.SecHandHouseDataPipeline':500,} 
    }
    # start_urls = ['https://bj.lianjia.com/ershoufang/pg1/']

    def start_requests(self):
        base_url = 'https://bj.lianjia.com/ershoufang/pg'
        for page in range(3,8):
            yield Request(url=base_url+str(page)+'/',callback=self.parse)

    def parse(self, response):
        item=SecHandHouseData()

        document = BeautifulSoup(response.text,features="lxml")
        for node in document.select('.sellListContent > li'):
            try:
                item['name'] = node.select('.title > a')[0].text
                item['type'] = node.select('.houseInfo')[0].text
                item['location'] = '/'.join(res.text for res in node.select('.positionInfo > a'))
                item['unit_price'] = node.select('.unitPrice > span')[0].text
                item['total_price'] = node.select('.totalPrice > span')[0].text + '万'
            except Exception:
                pass
            
            yield(item)
            # name = scrapy.Field()
            # location = scrapy.Field()
            # type = scrapy.Field()
            # per_price = scrapy.Field()
            # total_price = scrapy.Field()