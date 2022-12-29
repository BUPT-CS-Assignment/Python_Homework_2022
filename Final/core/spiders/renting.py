import scrapy
from scrapy import Request
from core.items import *
from bs4 import BeautifulSoup as BS
import json
from copy import deepcopy
from core.base import city_name

class RentingSpider(scrapy.Spider):
    name = 'cbd_sipder'
    city = ''
    total = 0
    allowed_domains=['lianjia.com']
    custom_settings = {
        'ITEM_PIPELINES':{'core.pipelines.RentingPipeline':500,} 
    }
    cbd_data = []
    
    
    def __init__(self, city):
        super().__init__()
        self.city = city
        
    def start_requests(self):
        # 读取CBD数据
        with open(f'data/citys/{self.city}/cbd.json','r',encoding='utf-8') as f:    
            self.cbd_data = json.load(f)    
            f.close()
        for item in self.cbd_data:
            url = item['url']
            pages = item['pages']
            
            print(f'crawling renting info in cbd {city_name[self.city]}--{item["name"]}, expected total {item["total"]}')
            if item["total"] > 3000:    # 针对大于3000的CBD，进行小区分类的重读取
                unit_url = str(url).replace('zufang','xiaoqu')
                params = {'cbd':deepcopy(item['name']), 'url':unit_url}
                yield Request(url=unit_url, callback=self.unit_requests,cb_kwargs=params)

            params = {'cbd':deepcopy(item['name'])}
            for i in range(1,pages + 1):
                yield Request(url=f'{url}pg{i}/',callback=self.parse,cb_kwargs=params)  # 遍历读取每页数据

    # 处理小区主页
    def unit_requests(self,response,cbd,url):
        doc = BS(response.text,features="lxml")
        total = doc.find('h2',class_='total fl').find('span').text.strip()
        print(f'* large CBD -- crawling by units, expected total {total}')
        
        page_box = doc.find('div',attrs={'comp-module':'page'}).attrs.get('page-data')
        page_box = json.loads(page_box)
        pages = page_box['totalPage']
        for i in range(1, pages + 1):
            yield Request(url=f'{url}pg{i}/', callback=self.parse_uints_page,cb_kwargs={'cbd':cbd}) # 遍历小区的每一页
    
    # 处理小区单页
    def parse_uints_page(self,response,cbd):
        doc = BS(response.text,features="lxml")
        for ele in doc.find('ul', class_='listContent').find_all('li'):
            node = ele.find('div', class_='houseInfo').find_all('a')[-1]
            url = node.attrs.get('href')
            if url == None:
                continue
            yield Request(url=url,callback=self.parse_uints,cb_kwargs={'cbd':cbd,'url':url})    # 读取该页每个小区租房页面
        
    # 处理小区租房页面
    def parse_uints(self, response, cbd, url):
        doc = BS(response.text,features="lxml")
        page_box = doc.find('div',class_='content__pg')
        if page_box == None:
            yield Request(url=url,callback=self.parse,cb_kwargs={'cbd':cbd})
        else:
            total_page = int(page_box.attrs.get('data-totalpage'))
            for i in range (1, total_page + 1):
                yield Request(url=f'{url}pg{i}/',callback=self.parse,cb_kwargs={'cbd':cbd}) # 遍历小区租房页面的每一页
    
    # 处理基本数据项
    def parse(self,response,cbd):
        doc = BS(response.text,features="lxml")
        for ele in doc.find('div',class_='content__list').select('.content__list--item'):
            id = ele.attrs.get('data-house_code')
            ad_code = ele.attrs.get('data-ad_code')

            name = ele.find('p',class_='content__list--item--title').text.strip()
            brand = ele.find('span', class_='brand')
            brand = brand.text.strip() if brand != None else '链家' # 未指定品牌，默认为链家
            price = ele.find('span', class_='content__list--item-price').text.replace('\n','').strip()  

            des = ele.find('p',class_='content__list--item--des').text.replace('\n','').replace('  ','')

            item = RentingItem()
            item['id'] = id
            item['name'] = name
            item['city'] = self.city
            item['cbd'] = cbd
            item['ad_code'] = ad_code
            item['brand'] = brand
            item['price'] = price
            item['addition'] = des

            yield item



