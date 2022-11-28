import scrapy
from scrapy import Request
from task1.items import *
from bs4 import BeautifulSoup

class NewHouseSpider(scrapy.Spider):
    name = 'new'
    allowed_domains = ['bj.fang.lianjia.com']
    custom_settings = {
        'ITEM_PIPELINES':{'task1.pipelines.NewHouseDataPipeline':500,} 
    }
    # start_urls = ['https://bj.fang.lianjia.com/loupan/pg1/']

    def start_requests(self):
        base_url = 'https://bj.fang.lianjia.com/loupan/pg'
        for page in range(3,8):
            yield Request(url=base_url+str(page)+'/',callback=self.parse)
            

    def parse(self, response):
        document = BeautifulSoup(response.text,features="lxml")
        for node in document.select('.resblock-desc-wrapper'):
            item=NewHouseData()
            item['name'] = node.select('.name')[0].text
            item['type'] = node.find('span',class_ = 'resblock-type').text
            loc_node = node.select('.resblock-location')[0]
            item['location'] = '/'.join(res.text for res in loc_node.find_all('span')) + '/' + loc_node.find('a').text
            item['room'] = '/'.join(res.text for res in node.select('.resblock-room > span')) 
            item['area'] = node.select('.resblock-area > span')[0].text[3:]
            price_node = node.select('.resblock-price')[0]
            item['unit_price'] = price_node.find('span',class_='number').text + price_node.find('span',class_='desc').text[1:]
            try:
                item['total_price'] = price_node.find(class_ = 'second').text[2:]
            except Exception:
                item['total_price'] = ''

            yield(item)