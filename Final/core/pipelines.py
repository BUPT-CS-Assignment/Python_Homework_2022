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


class CBDPipeline:
    data = {}
    def __init__(self):
        for city in citys:
            self.data[city] = []
            
    def open_spider(self,spider):
        print(f'crawling cbd info in {city_name[spider.city]}')
    
    def process_item(self,item,spider):
        node = dict(item)
        if next((x for x in self.data[node['city']] if x['name'] == node['name']),None) == None:
            self.data[node['city']].append(node)
        return item

    def close_spider(self,spider):
        city = spider.city
        with open(f'data/citys/{city}/cbd.json','w',encoding='utf-8') as f:
            json.dump(self.data[city],f,indent=4,ensure_ascii=False)
            f.close()   
        print(f'finish in {city_name[city]}')


class RentingPipeline:
    db = database()
    def open_spider(self,spider):
        city = spider.city
        print(f'crawling renting info in {city_name[city]}')
        # with open(f'data/{city}/renting.json','w','utf-8') as f:
        #     f.write('[')
        #     f.close()
             
    def process_item(self,item,spider):
        item = dict(item)
        # json_str = json.dumps(node,ensure_ascii=False)
        # with open(f'data/{node["city"]}/renting.json','a','utf-8') as f:
        #     f.write(json_str + ',\n')
        #     f.close()
        # return item
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
        # with open(f'data/{city}/renting.json','rb+','utf-8') as f:
        #     f.seek(-3,2)
        #     f.write(']'.encode())
        #     f.close()