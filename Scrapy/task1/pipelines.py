# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

class NewHouseDataPipeline:
    json_list = []
    
    def process_item(self, item, spider):
        self.json_list.append(dict(item))
        return item
    
    def close_spider(self,spider):
        with open('task1/data/new_house.json','w',encoding='utf-8') as f:
            json.dump(self.json_list,f,indent=4,ensure_ascii=False)

class SecHandHouseDataPipeline:
    json_list = []

    def process_item(self, item, spider):
        self.json_list.append(dict(item))
        return item
    
    def close_spider(self,spider):
        with open('task1/data/sec_hand_house.json','w',encoding='utf-8') as f:
            json.dump(self.json_lst,f,indent=4,ensure_ascii=False)
