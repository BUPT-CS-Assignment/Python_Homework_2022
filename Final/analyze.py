import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sen
import pandas as pd
import numpy as np
from pyecharts.charts import Grid
from pyecharts.charts import Geo
from pyecharts.charts import Bar
from pyecharts.charts import Radar
from pyecharts import options as opts
from pyecharts.globals import GeoType
from core.base import citys, city_name
import json
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def plot_counts():
    df = pd.read_csv(f'data/renting.csv')
    df_origin = df.groupby(['city'])['id'].count().reset_index(name='count')
    df_max = df_origin.max()['count']
    df_lj = df[df['ad'] == 0].groupby(['city']).count()['id'].reset_index(name='count')
    df_ad = df.groupby(['city'])['ad'].apply(lambda x:(x==1).sum()).reset_index(name='count')
    city_part = list(df_lj['city'])

    r = Radar(init_opts=opts.InitOpts(width='900px',height='700px'))
    r.add_schema(
        schema=[opts.RadarIndicatorItem(name=n, max_=int(df_max)) for n in city_part],
        splitarea_opt=opts.SplitAreaOpts(is_show=True,areastyle_opts=opts.AreaStyleOpts(opacity=1))
    )
    r.add('链家房源',[list(df_lj['count'])],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.2),
        linestyle_opts=opts.LineStyleOpts(width=2),
        label_opts=opts.LabelOpts(position='top',font_size=13,font_weight='bold',color= '#696969'),
        color='#708090')
    r.add('广告房源',[list(df_ad['count'])],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.2),
        linestyle_opts=opts.LineStyleOpts(width=2),
        color='#F08080',
        label_opts=opts.LabelOpts(is_show=False))
    r.set_global_opts(
        title_opts=opts.TitleOpts(title='各城市租房数据',subtitle='data from lianjia.com'),
        legend_opts=opts.LegendOpts()
    )
    r.render('data/images/counts.html')

def plot_price_all():
    plot_price(True)
    plot_price(False)

def plot_price(ad=True):
    data_price = analyze_price('price',ad)
    data_unit = analyze_price('unit_price',ad)
    label = {'amax':{'tag':'最大值','color':'#B22222'},
        'average':{'tag':'平均值','color':'#FFA500'},
        'median':{'tag':'中位数','color':'#4682B4'},
        'amin':{'tag':'最小值','color':'#5F9EA0'},
    }
    b_top = Bar()
    b_top.add_xaxis(data_price['city'])
    for key in data_price:
        if key == 'city': continue
        b_top.add_yaxis(f'{label[key]["tag"]}{"/10" if key == "amax" else ""} (元)', data_price[key],
            itemstyle_opts=opts.ItemStyleOpts(color=label[key]["color"]))

    b_top.set_global_opts(
        legend_opts=opts.LegendOpts(selected_mode="mutiple",orient="vertical",pos_top="5%",pos_left='right'),
        title_opts=opts.TitleOpts(title=f'各城市(单位面积)月租金数据分布{"[所有房源]" if ad else "[链家房源]"}',subtitle='data from lianjia.com',pos_left='5%'),
        xaxis_opts=opts.AxisOpts(name='城市',position='bottom',
                                name_textstyle_opts=opts.TextStyleOpts(font_weight='bold'),
                                axislabel_opts=opts.LabelOpts(font_weight='bold',font_size=13)),
        yaxis_opts=opts.AxisOpts(name='月租金',name_textstyle_opts=opts.TextStyleOpts(font_weight='bold'))
    )
    b_bottom = Bar()
    b_bottom.add_xaxis(['' for i in range(len(data_price['city']))])
    for key in data_unit:
        if key == 'city': continue
        b_bottom.add_yaxis(f'{label[key]["tag"]} (元/平米)', data_unit[key],
            itemstyle_opts=opts.ItemStyleOpts(color=label[key]["color"]))

    b_bottom.set_global_opts(
        legend_opts=opts.LegendOpts(selected_mode="mutiple",orient="vertical",pos_top="56%",pos_left='right'),
        xaxis_opts=opts.AxisOpts(position='top'),
        yaxis_opts=opts.AxisOpts(name='单位面积月租金',is_inverse=True,name_textstyle_opts=opts.TextStyleOpts(font_weight='bold'))
    )
    grid = Grid(init_opts=opts.InitOpts(width='1200px',height='770px'))
    grid.add(b_top,grid_opts=opts.GridOpts(pos_top='12%',pos_bottom='50%'))
    grid.add(b_bottom,grid_opts=opts.GridOpts(pos_top='56%'))
    grid.render(f'data/images/price/price({"all" if ad else "lianjia"}).html')


def analyze_price(col = 'price',ad = True):
    if col != 'price' and col != 'unit_price':
        return None
    df = pd.read_csv(f'data/renting.csv')
    if not ad: df = df[df['ad'] == 0]
    data = {'city':[],'amax':[],'average':[],'median':[],'amin':[]}
    res = df[df[col] > 0].groupby('city')[col].agg([np.average,np.max,np.min,np.median]).reset_index()
    for key in data:
        if col == 'price':
            data[key] = list(map(lambda x:int(x/10) if key == 'amax' else int(x),res[key]) if key != 'city' else res[key])
        else:
            data[key] = list(map(lambda x:float(format(x,'.1f')),res[key]) if key != 'city' else res[key])
    return data
    # bar_width = 0.2
    # num = 0
    # plt.figure()
    # for key in data:
    #     if key == 'city': continue
    #     plt.bar(np.arange(5) + num * bar_width, data[key],label=key,width=bar_width)
    #     num += 1
    
    # plt.title(f'各城市{"单位面积" if col == "unit_price" else ""}月租房价格情况{"(含广告数据)" if ad else ""}')
    # plt.xticks(np.arange(5) + 2 * bar_width,data['city'])
    # plt.legend(loc='best')
    # plt.show()

def plot_cbd_citys():
    for city in citys:
        plot_cbd(city)

def plot_cbd(city):
    g = Geo(init_opts=opts.InitOpts(width='1500px',height='750px'))
    g.add_schema(maptype=city_name[city])

    with open(f'data/citys/{city}/position.json','r',encoding='utf-8') as f:
        data = json.load(f)
    
    for ele in data:
        g.add_coordinate(ele['name'],ele['x'],ele['y'])
    
    df = pd.read_csv(f'data/renting.csv')
    df = df[df['city'] == city_name[city]]
    res = df.groupby(['cbd']).agg({'price':np.average}).reset_index()
    data_pair = []
    for i in range(len(res)):
        data_pair.append((res.loc[i,'cbd'],int(res.loc[i,'price'])))
    data_pair.sort(key=lambda x:x[1])

    g.add('',data_pair,type_=GeoType.EFFECT_SCATTER,symbol_size=5)
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # color map
    pieces = generate_color(res['price'].max())
    g.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
        title_opts=opts.TitleOpts(title=f'{city_name[city]}市平均月租房价格',subtitle=f'data from {city}.lianjia.com',pos_left='5%')
    )

    g.render(f'data/images/cbd/{city}.html')

def generate_color(max):
    res = []
    cur = 0
    path = 1000
    while cur <= max:
        res.append({'min':cur,'max':cur + path,'color':'#'})
        cur += path
        path = 100000 if cur >= 100000 else (10000 if cur >= 10000 else 1000)

    cmap = mpl.cm.get_cmap('RdYlBu_r',len(res))(range(len(res)))
    for i in range(len(res)):
        rgb = cmap[i]
        code = '#'
        for j in range(3):
            code += str(hex(int(rgb[j]*255)))[-2:].replace('x','0').upper()
        res[i]['color'] = code
    return res
