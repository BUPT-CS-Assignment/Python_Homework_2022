import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sen
import pandas as pd
import numpy as np
# from pyecharts.charts import Grid
# from pyecharts.charts import Geo
# from pyecharts.charts import Bar
# from pyecharts.charts import Bar3D
# from pyecharts.charts import Radar
# from pyecharts.charts import HeatMap
from pyecharts.charts import *
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.globals import GeoType
from pyecharts.globals import SymbolType
from core.base import citys, city_name
import json
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False



def plot():
    plot_price_types()
    plot_counts()
    plot_price_all()
    plot_cbd_citys()
    plot_room_citys()
    plot_orien_citys()
    plot_types()
    plot_gdp_citys()
    return

def plot_gdp_citys():
    with open('data/gdp.json','r',encoding='utf-8') as f:
        gdp_file = json.load(f)
    data = analyze_price(col = 'unit_price',ad = True)
    gdp = [gdp_file[key]['gdp'] for key in data['city']]
    salary = [gdp_file[key]['salary'] for key in data['city']]

    b = Bar(init_opts=opts.InitOpts(width='1100px',height='550px'))
    b.add_xaxis(data['city'])
    b.add_yaxis(series_name='单位面积月租金中位数',y_axis=data['median'],itemstyle_opts=opts.ItemStyleOpts(color='#4169E1'),z=0)
    b.add_yaxis(series_name='单位面积月租金平均数',y_axis=data['average'],itemstyle_opts=opts.ItemStyleOpts(color='#3CB371'),z=0)
    b.extend_axis(
        yaxis=opts.AxisOpts(name='人均GDP',name_textstyle_opts=opts.TextStyleOpts(font_weight='bold'),position="right")
    )
    b.extend_axis(
        yaxis=opts.AxisOpts(name='月均工资/元',max_=max(salary)+10000,name_textstyle_opts=opts.TextStyleOpts(font_weight='bold'),position="right",offset=60,
        axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFA500")))
    )
    b.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    b.set_global_opts(
        legend_opts=opts.LegendOpts(selected_mode="mutiple",orient="horizontal",pos_bottom="bottom",pos_left='center'),
        title_opts=opts.TitleOpts(title="各城市人均GDP、月平均工资与单位面积月租金分布概览",subtitle='data from lianjia.com',pos_left='%5'),
        yaxis_opts=opts.AxisOpts(name='',max_=max(data['average']) + 50,
            axislabel_opts=opts.LabelOpts(formatter="{value} 元/平米"),
            name_textstyle_opts=opts.TextStyleOpts(font_weight='bold')),
        xaxis_opts=opts.AxisOpts(name='',position='bottom',axislabel_opts=opts.LabelOpts(font_weight='bold',font_size=13))
    )
    
    l = Line(init_opts=opts.InitOpts(width='1100px',height='550px'))
    l.add_xaxis(data['city'])
    l.add_yaxis('人均GDP',y_axis=gdp,yaxis_index=1,itemstyle_opts=opts.ItemStyleOpts(color='#B22222'),
        label_opts=opts.LabelOpts(font_weight='bold'),
        symbol_size=15,symbol='circle',
        linestyle_opts=opts.LineStyleOpts(width=2, type_="dashed"))

    l2 = Line(init_opts=opts.InitOpts(width='1100px',height='550px'))
    l.add_xaxis(data['city'])
    l.add_yaxis('月平均工资',y_axis=salary,yaxis_index=2,itemstyle_opts=opts.ItemStyleOpts(color='#FFA500'),
        label_opts=opts.LabelOpts(font_weight='bold'),
        symbol_size=15,symbol='circle',
        linestyle_opts=opts.LineStyleOpts(width=2,type_="dashed"))

    b.overlap(l)
    b.overlap(l2)
    b.render('data/images/gdp-salary.html')

    


def plot_price_types(origin = False):
    data = analyze_price_types(origin)
    for type in data['types']:
        s = Scatter()
        s.add_xaxis(xaxis_data=data[type]['area'])
        s.add_yaxis(series_name=type,y_axis=data[type]['price'],symbol_size = 5,label_opts=opts.LabelOpts(is_show=False))
        s.set_series_opts()
        s.set_global_opts(
            xaxis_opts=opts.AxisOpts(name='area',
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(name='price',
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            visualmap_opts=opts.VisualMapOpts(max_=max(data[type]['price'])+500,
                range_color=["#313695","#4575B4","#74ADD1","#FEE090","#FDAE61","#F46D43","#D73027"],
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title=f"{type}类型数据分布",subtitle='data from lianjia.com',pos_left="5%"),
        )
        grid = Grid()
        grid.add(s,grid_opts=opts.GridOpts(pos_top='15%'))
        grid.render(f'data/images/type/{type}{"_origin" if origin else ""}.html')
    

def analyze_price_types(origin):
    df = pd.read_csv(f'data/renting{"_origin" if origin else "" }.csv')
    type = list(df['type'].unique())
    data = {}
    for t in type:
        data[t] = {'price':[],'area':[]}
        res = df[(df['type'] == t) & (df['price'] > 0) & (df['area'] > 0)]
        for index,row in res.iterrows():
            data[t]['price'].append(row['price'])
            data[t]['area'].append(row['area'])
    data['types'] = type
    return data


def plot_types():
    data = analyze_type()
    p = Pie(init_opts=opts.InitOpts(width='800px',height='700px'))
    p.add(series_name='租房类型',data_pair=data,radius=["40%", "60%"],
        label_opts=opts.LabelOpts(
            position="outside",
            formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            background_color="#eee",border_color="#aaa",
            border_width=1,border_radius=4,
            rich={
                "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                "abg": {"backgroundColor": "#e3e3e3","width": "100%","align": "right","height": 22,
                    "borderRadius": [4, 4, 0, 0],},
                "hr": {"borderColor": "#aaa","width": "100%","borderWidth": 0.5,"height": 0,},
                "b": {"fontSize": 16, "lineHeight": 33},
                "per": {"color": "#eee","backgroundColor": "#334455","padding": [2, 4],"borderRadius": 2,},
            },
        ),
    )
    p.set_colors(["#313695","#4575B4","#74ADD1","#FDAE61","#F46D43","#D73027"])
    p.set_global_opts(
        title_opts=opts.TitleOpts(title="数据源租房类型概览",subtitle='data from lianjia.com',pos_left="5%"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )
    p.render('data/images/type.html')


def analyze_type():
    df = pd.read_csv(f'data/renting.csv')
    res = df.groupby(['type'])['id'].count().reset_index(name='count')
    data = []
    for index,row in res.iterrows():
        data.append([row['type'],row['count']])
    return data


def plot_brands_citys():
    for city in citys:
        plot_brands(city)

def plot_brands(city):
    data = analyze_brands(city)
    w = WordCloud()
    w.add('',data,word_size_range=[15,100],shape=SymbolType.RECT)
    w.set_global_opts(
        title_opts=opts.TitleOpts(title=f'{city_name[city]}市链家官网房源统计',subtitle=f'data from {city}.lianjia.com')
    )
    w.render(f'data/images/brand/{city}.html')

def analyze_brands(city):
    df = pd.read_csv(f'data/renting.csv')
    df = df[df['city'] == city_name[city]]
    res = df.groupby(['brand'])['id'].count().reset_index(name='count')
    data = []
    for index,row in res.iterrows():
        data.append((row['brand'],row['count']))
    return data


def plot_orien_citys():
    orien = ['北','东北','东','东南','南','西南','西','西北']
    data = []
    min_v = 5000
    max_v = 0
    m = 0
    for city in citys:
        cdata = analyze_orien(city)
        n = 0
        for o in orien:
            data.append([n,m,cdata[o]])
            if cdata[o] < min_v: min_v = cdata[o]
            if cdata[o] > max_v: max_v = cdata[o]
            n += 1
        m += 1
    h = HeatMap(init_opts=opts.InitOpts(width='1200px',height='700px'))
    h.add_xaxis(xaxis_data=orien)
    h.add_yaxis(series_name='月租金/元',yaxis_data=[city_name[city] for city in citys],value=data,
            label_opts=opts.LabelOpts(is_show=True, color="#191970", position="insideBottom",font_weight = 'bold', horizontal_align="50%")
        )
    h.set_global_opts(
        xaxis_opts=opts.AxisOpts(name='朝向',type_='category',splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)),
            name_textstyle_opts=opts.TextStyleOpts(font_weight='bold',font_size=13)),
        yaxis_opts=opts.AxisOpts(name='城市',type_='category',splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)),
            name_textstyle_opts=opts.TextStyleOpts(font_weight='bold',font_size=13)),
        visualmap_opts=opts.VisualMapOpts(
            min_=min_v - 500, max_=max_v + 500, is_calculable=True, orient="vertical", pos_left="left",
            range_color=["#313695","#4575B4","#74ADD1","#ABD9E9","#E0F3F8","#FFFFbF","#FEE090","#FDAE61","#F46D43","#D73027",],
        ),
        title_opts=opts.TitleOpts(title='各城市不同朝向平均月租金数据分布[中位数]',subtitle='data from lianjia.com'),
        legend_opts=opts.LegendOpts(is_show=False)
        
    )
    grid = Grid(init_opts=opts.InitOpts(width='1200px',height='720px'))
    grid.add(h,grid_opts=opts.GridOpts(pos_top='15%'))
    grid.render('data/images/orien.html')



def analyze_orien(city):
    df = pd.read_csv(f'data/renting.csv')
    df = df[df['city'] == city_name[city]]
    orien = ['北','东北','东','东南','南','西南','西','西北']
    df['orien'] = df['orien'].apply(lambda x: '' if x != x else x)
    data = {}
    for pos in orien:
        num = df[df['orien'].str.contains(f'/{pos}/')].copy()
        num['price'] = num['price'].apply(lambda x:0 if x != x else int(x))
        num.drop(num[num['price'] <= 0].index,inplace=True)
        num = num['price'].median(axis=0)
        data[pos] = int(num)
    return data


def plot_room_citys():
    origin = {}
    for city in citys:
        origin[city] = analyze_room(city)
    
    data = []
    for i in range(1,5):
        n = 0
        for city in citys:
            tmp = origin[city][str(i)]
            m = 0
            for key in tmp:
                data.append([(i-1)*5+n,m,tmp[key] if key != 'max' else int(tmp[key]/10)])
                m += 1
            n += 1
    label = []
    for tag in ['\n一居','\n二居','\n三居','\n四居及以上']:
        for city in citys:
            label.append(city_name[city] + tag if city == 'bj' else city_name[city])

    b = Bar3D(init_opts=opts.InitOpts(width='1500px',height='750px'))
    b.add(
        series_name='月租金',
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(name='城市及户型',type_='category',data=label,interval=0,
            margin=2,textstyle_opts=opts.TextStyleOpts(font_weight='bold',font_size=13)),
        yaxis3d_opts=opts.Axis3DOpts(name='数据类型',type_='category',data=['最小值(元)','中位数(元)','平均值(元)','最大值(十元)'],
            margin=2,textstyle_opts=opts.TextStyleOpts(font_weight='bold',font_size=13)),
        zaxis3d_opts=opts.Axis3DOpts(name='月租金',type_='value',textstyle_opts=opts.TextStyleOpts(font_weight='bold',font_size=13))
    )
    b.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(max_=50000,
            range_color=["#313695","#4575B4","#74ADD1","#ABD9E9","#E0F3F8","#FFFFbF","#FEE090","#FDAE61","#F46D43","#D73027",],
        ),
        title_opts=opts.TitleOpts(title='各城市不同户型月租金数据分布',subtitle='data from lianjia.com'),
        legend_opts=opts.LegendOpts()
    )

    b.render('data/images/room.html')



def analyze_room(city):
    df = pd.read_csv(f'data/renting.csv')
    df = df[df['city'] == city_name[city]]
    func = ['min','median','average','max']
    res1 = df[df['room'] == 1]['price'].agg(func).reset_index()
    res2 = df[df['room'] == 2]['price'].agg(func).reset_index()
    res3 = df[df['room'] == 3]['price'].agg(func).reset_index()
    res4 = df[df['room'] >= 4]['price'].agg(func).reset_index()
    res = [None,res1,res2,res3,res4]
    data={}
    for i in range(1,5):
        tmp = {}
        for key in func:
            tmp[key] = int(res[i][res[i]['index'] == key]['price'])
        data[str(i)] = tmp
    data['city'] = city_name[city]
    return data

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
        title_opts=opts.TitleOpts(title='各城市租房数据源概览',subtitle='data from lianjia.com'),
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
        title_opts=opts.TitleOpts(title='各城市月租金额数据概览',subtitle=f'{"所有房源" if ad else "链家房源"} -- data from lianjia.com',pos_left='5%'),
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
    df = df[(df['type'] == '整租') | (df['type'] == '独栋')]
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
