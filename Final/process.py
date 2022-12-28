from sql.database import database
from core.base import citys
from core.base import city_name
import pandas as pd
import pandas.io.sql as pd_sql 
import numpy as np
import re

def init_db():
    db = database()
    for city in citys:
        sql = f'drop table {city};'
        try:
            db.exec(sql)
        except Exception:
            pass
        
        sql = f'''
            create table {city} (
                id text,
                name text,
                cbd text,
                ad_code text,
                brand text,
                price text,
                addition text,
                primary key(id)
            );
        '''
        db.exec(sql)
    db.close()

def check_db():
    db = database()
    for city in citys:
        sql = f'select count(*) from {city}'
        res = db.select(sql)
        print(f'crawled distinct infomation in {city_name[city]} counts {res[0][0]}')
    db.close()


def export_csv():
    db = database()
    for city in citys:
        sql = f'select * from {city};'
        data_frame = pd_sql.read_sql(sql,db.conn)
        df = data_frame.sort_values(by=['cbd','ad_code','brand'],ignore_index=True)
        df.to_csv(f'data/citys/{city}/renting.csv')

def exception_process():
    df = pd.read_csv(f'data/renting_origin.csv')
    df.drop(df[df['area'] > 1000].index, inplace=True)
    df.drop(df[df['unit_price'] <= 1].index,inplace=True)
    df.drop(df[(df['area'] >= 200) & (df['price'] <= 1500)].index,inplace=True)

    df.to_csv('data/renting.csv')

def extract():
    df_new = pd.DataFrame(columns=['id','name','city','cbd','brand','type','area','orien','room','price','unit_price','ad'])
    for city in citys:
        print(f'processing data for city {city}')
        df = pd.read_csv(f'data/citys/{city}/renting.csv')
        df.insert(4,'city',city_name[city])
        df['type'],df['price'],df['area'],df['orien'],df['room'],df['unit_price'],df['ad'] = zip(*df.apply(lambda x:ext_function(x),axis=1))
        df_new = pd.concat([df_new,df],join='inner', ignore_index=True)
    
    df_new = df_new.sort_values(by=['city','cbd','ad','brand'],ignore_index=True)


    # drop invalid
    df_new.drop(df_new[(df_new['price'] == 0) | (df_new['price'] != df_new['price'])].index,inplace=True)
    df_new.drop(df_new[df_new['room'] <= 0].index,inplace=True)
    df_new.drop(df_new[(df_new['area'] <= 0) | (df_new['area'] != df_new['area'])].index, inplace=True)
    

    df_new.to_csv(f'data/renting_origin.csv')
    print('extract finish.')

def ext_function(row):
    type = process_type(row['name'])
    add = process_addition(row['addition'])
    price = process_price(row['price'])
    unit_price = price/add['area'] if add['area'] > 0 else 0
    return type,price,add['area'],add['orien'],add['room'],unit_price,is_ad(row['id'],row['ad_code'])


def is_ad(id,ad_code):
    if re.match('[A-Z]+[0-9]+',id) is None:
        return 1
    return 0 if str(ad_code) == '0' else 1

def process_type(input):
    type = re.match('((整租)|(合租)|(独栋)).',input)
    if type != None:
        if (str(type.group(1))) not in ['整租','合租','独栋']:
            print(type.group(1))
        return str(type.group(1))
    else:
        return "未知"


def process_price(input):
    price = re.match('([0-9\-\.]+) 元/月',input)
    if price == None:
        return 0
    price = list(map(int,price.group(1).split('-')))
    avg = np.average(np.array(price))
    return int(avg)

def process_addition(input):
    detail = {
        'area':0,
        'orien':'',
        'room':0,
    }
    area = re.search('([0-9\-\.]+)㎡',input)
    if area != None:
        area = list(map(float,str(area.group(1)).split('-')))
        avg = np.average(np.array(area))
        detail['area'] = avg
    
    room = re.search('([0-9]+)室([0-9]+)厅([0-9]+)卫',input)
    if room != None:
        detail['room'] = int(room.group(1)) if int(room.group(3)) > 0 else -1

    orien = re.search('/[东西南北]+(\s{1}[东西南北]+)*/',input)
    if orien != None:
        detail['orien'] = '/' + '/'.join(orien.group()[1:-1].split()) + '/'

    return detail
