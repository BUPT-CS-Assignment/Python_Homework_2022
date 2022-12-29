from sql.database import database
from core.base import citys
from core.base import city_name
import pandas as pd
import pandas.io.sql as pd_sql 
import numpy as np
import re


'''
----------------------------- 数据库操作 -----------------------------
'''

def init_db():
    db = database()
    for city in citys:
        sql = f'drop table {city};' # 删除旧数据表
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

# 查看抓取的数据情况
def check_db(): 
    db = database()
    for city in citys:
        sql = f'select count(*) from {city}'
        res = db.select(sql)
        print(f'crawled distinct infomation in {city_name[city]} counts {res[0][0]}')
    db.close()


'''
----------------------------- 数据处理 -----------------------------
'''
# 原始数据csv导出
def export_csv():
    db = database()
    for city in citys:
        sql = f'select * from {city};'
        data_frame = pd_sql.read_sql(sql,db.conn)
        df = data_frame.sort_values(by=['cbd','ad_code','brand'],ignore_index=True)
        df.to_csv(f'data/citys/{city}/renting.csv')


# 数据预处理汇总
def extract():
    df_new = pd.DataFrame(columns=['id','name','city','cbd','brand','type','area','orien','room','price','unit_price','ad'])
    for city in citys:
        print(f'processing data for city {city}')
        df = pd.read_csv(f'data/citys/{city}/renting.csv')
        df.insert(4,'city',city_name[city]) # 后续需要汇总到一张表，因此插入城市字段
        df['type'],df['price'],df['area'],df['orien'],df['room'],df['unit_price'],df['ad'] = zip(*df.apply(lambda x:ext_function(x),axis=1))
        df_new = pd.concat([df_new,df],join='inner', ignore_index=True) # 数据表连接
    
    df_new = df_new.sort_values(by=['city','cbd','ad','brand'],ignore_index=True)                           # 按照城市、CBD、广告、数据源进行排序

    # drop invalid
    df_new.drop(df_new[(df_new['price'] <= 0) | (df_new['price'] != df_new['price'])].index,inplace=True)   # 删除价格为0的数据
    df_new.drop(df_new[df_new['room'] <= 0].index,inplace=True)                                             # 删除户型为0的数据
    df_new.drop(df_new[(df_new['area'] <= 0) | (df_new['area'] != df_new['area'])].index, inplace=True)     # 删除面积为0的数据

    df_new.to_csv(f'data/renting_origin.csv',index=False)
    print('extract finish.')

# 数据切分apply()函数
def ext_function(row):
    type = process_type(row['name'])            # 租房类型
    add = process_addition(row['addition'])     # 附加数据
    price = process_price(row['price'])         # 价格
    unit_price = price/add['area'] if add['area'] > 0 else 0    # 单位面积价格
    return type,price,add['area'],add['orien'],add['room'],unit_price,is_ad(row['id'],row['ad_code'])


# 异常信息处理
def exception_process():
    df = pd.read_csv('data/renting_origin.csv')
    df = df.drop(df[df['unit_price'] < 3].index)                            # 删除单位面积价格小于3的数据
    df = df.drop(df[(df['area'] >= 200) & (df['price'] <= 1500)].index)     # 删除面积大于200而月租金小于1500元的数据
    df.to_csv('data/renting.csv',index=False)


'''
----------------------------- 功能性函数 -----------------------------
'''

# 广告判断
def is_ad(id,ad_code):
    if re.match('[A-Z]+[0-9]+',id) is None:
        return 1
    return 0 if str(ad_code) == '0' else 1

# 租房类型判断
def process_type(input):
    type = re.match('((整租)|(合租)|(独栋)).',input)    # 正则提取
    if type != None:
        if (str(type.group(1))) not in ['整租','合租','独栋']: 
            print(type.group(1))
        return str(type.group(1))
    else:
        return "未知"

# 金额判断
def process_price(input):
    price = re.match('([0-9\-\.]+) 元/月',input)    # 正则提取
    if price == None:
        return 0
    price = list(map(int,price.group(1).split('-')))    # 对于范围，计算平均值
    avg = np.average(np.array(price))
    return int(avg)

# 长信息拆分
def process_addition(input):
    detail = {          # 输出字典
        'area':0,
        'orien':' ',
        'room':0,
    }
    area = re.search('([0-9\-\.]+)㎡',input)    # 面积处理
    if area != None:
        area = list(map(float,str(area.group(1)).split('-')))
        avg = np.average(np.array(area))        # 对于范围， 取其均值
        detail['area'] = avg
    
    room = re.search('([0-9]+)室([0-9]+)厅([0-9]+)卫',input)    # 户型处理
    if room != None:
        detail['room'] = int(room.group(1)) if int(room.group(3)) > 0 else 0

    orien = re.search('/[东西南北]+(\s{1}[东西南北]+)*/',input)     # 朝向处理
    if orien != None:
        detail['orien'] = '/' + '/'.join(orien.group()[1:-1].split()) + '/'

    return detail
