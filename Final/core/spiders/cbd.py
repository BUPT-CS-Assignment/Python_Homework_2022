import scrapy
from scrapy import Request
from core.items import *
from bs4 import BeautifulSoup as BS
from copy import deepcopy

class CBDSpider(scrapy.Spider):
    name = 'cbd_sipder'
    city = ''
    allowed_domains=['lianjia.com']
    custom_settings = {
        'ITEM_PIPELINES':{'core.pipelines.CBDPipeline':500,} 
    }
    
    def __init__(self, city):
        super().__init__()
        self.city = city
    
    def start_requests(self):
        yield Request(url=f'https://{self.city}.lianjia.com/zufang/',callback=self.parse_region)
    
    def parse_region(self, response):
        doc = BS(response.text,features="lxml")
        params = {}
        for node in doc.find('ul',attrs={'data-target':'area'}).select('.filter__item--level2'):
            if node.attrs.get('data-id') == '0':
                continue
            params['region'] = node.find('a').text
            href = node.find('a').attrs.get('href')
            yield Request(url=f'https://{self.city}.lianjia.com{href}',callback=self.parse_cbd_pre,cb_kwargs=params)
            
    def parse_cbd_pre(self, response, region):
        doc = BS(response.text,features="lxml")
        for node in doc.select('.filter__item--level3'):
            if node.attrs.get('data-id') == '0':
                continue
            item = CBDItem()
            item['city'] = self.city
            item['region'] = region
            item['name'] = node.find('a').text
            href = node.find('a').attrs.get('href')
            item['url'] = f'https://{self.city}.lianjia.com{href}'
            params={'item':deepcopy(item)}
            yield Request(url=f'https://{self.city}.lianjia.com{href}',callback=self.parse_cbd,cb_kwargs=params)
            
    def parse_cbd(self, response, item):
        doc = BS(response.text,features="lxml")
        item['total'] = int(doc.find('span',class_='content__title--hl').text)
        if item['total'] > 0:
            item['pages'] = int(doc.find('div',class_='content__pg').attrs.get('data-totalpage'))
            yield item
    
        
            