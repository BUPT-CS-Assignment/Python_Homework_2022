# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import time
import sqlite3
from core.base import citys,city_name
from sql.database import database

# CBD板块 pipeline
class CBDPipeline:
    data = {}       # 去重信息集合
    def __init__(self):
        for city in citys:
            self.data[city] = []    # 空值初始化
            
    def open_spider(self,spider):
        print(f'crawling cbd info in {city_name[spider.city]}')
    
    def process_item(self,item,spider):
        node = dict(item)   # 字典化
        if next((x for x in self.data[node['city']] if x['name'] == node['name']),None) == None:
            self.data[node['city']].append(node) # 去重插入
        return item

    def close_spider(self,spider):
        city = spider.city  # 城市标签
        # json 存储
        with open(f'data/citys/{city}/cbd.json','w',encoding='utf-8') as f:
            json.dump(self.data[city],f,indent=4,ensure_ascii=False)
            f.close()   
        print(f'finish in {city_name[city]}')


class RentingPipeline:
    db = database()
    def open_spider(self,spider):
        city = spider.city
        print(f'crawling renting info in {city_name[city]}')

             
    def process_item(self,item,spider):
        item = dict(item)
        sql = f'''
            insert into {spider.city} values(
                '{item['id']}',
                '{item['name']}',
                '{item['cbd']}',
                '{item['ad_code']}',
                '{item['brand']}',
                '{item['price']}',
                '{item['addition']}'
            );
        '''
        self.db.exec(sql)
    
    def close_spider(self,spider):
        city = spider.city        
        print(f'crawling finish for {city_name[city]}')
