import requests
import json
import time
from core.base import citys, city_name
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

def get_point(node):
    session = requests.session()
    city = city_name[node['city']]
    region = node['region']
    name = node['name']
    query = city + region + name
    url='https://apis.map.qq.com/jsapi'
    params = {
        'qt': 'geoc',
        'addr':query,
        'key':'UGMBZ-CINWR-DDRW5-W52AK-D3ENK-ZEBRC',
        'output':'jsonp',
        'pf': 'jsapi',
        'ref':'jsapi',
        'cb':'qq.maps._svcb3.geocoder0'
    }
    response = session.get(url=url, headers=headers, params=params)
    pos = response.text.find('"detail"')
    data = response.text[pos+9:-3]
    data = json.loads(data)
    try:
        return {'x':float(data['pointx']),'y':float(data['pointy'])}
    except Exception:
        print(f'not found: {query}')
        return {'x':-1,'y':-1}

def get_city_point(city):
    with open(f'../data/citys/{city}/cbd.json','r',encoding='utf-8') as f:
        origin = json.load(f)
    data = []
    for cbd in origin:
        point = get_point(cbd)
        data.append({
            'city':cbd['city'],
            'region':cbd['region'],
            'name':cbd['name'],
            'x':point['x'],
            'y':point['y']
        })
        time.sleep(0.1)

    with open(f'../data/citys/{city}/position.json','w',encoding='utf-8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
        f.close()   


def crawl_citys_position():
    for city in citys:
        print(f'crawling cbd positions in city {city_name[city]}')
        get_city_point(city)
        time.sleep(0.5)
    print('finish.')
