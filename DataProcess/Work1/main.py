import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import random

plt.rcParams['font.sans-serif']=['Simhei']
plt.rcParams['axes.unicode_minus'] = False

# format json
with open('data/new_house.json','r',encoding='utf-8') as f:
    raw = json.load(f)
for item in raw:
    item['name'].strip()                                                    # process location
    item['区域'],item['位置'],item['地点'] = item['location'].split('/')      # process name
    item.pop('location')
    item['room'] = item['room'].split('/')[0].strip()                       # process room
    item['area'] = int(np.mean(list(map(int,item['area'][:-1].split('-') if item['area'] != '' else [0])))) # process area
    # process total price
    item['total_price'],item['unit_price'] = item['unit_price'],item['total_price'] if item['total_price'] == '' else item['total_price'],item['unit_price']
    item['total_price'] = int(np.mean(list(map(int,item['total_price'].split('(')[0].split('-')))))
    item['unit_price'] = int(item['unit_price'].split('元')[0]) if item['unit_price'] != '' else int(item['total_price'] * 10000 / item['area'])

# data frame
data = pd.DataFrame.from_dict(raw)

def random_color(len):
    res = []
    [res.append('#' + ''.join([random.choice('0123456789abcdef') for j in range(6)])) for i in range(len)]
    return res;

# scatter
type = data['type'].unique()
colors = random_color(len(type) + 1)
# colors = ['#FF6347','#32CD32','#1E90FF','#7B68EE','#708090','#FFA500']
plt.figure()
plt.xlabel('总价/万元')
plt.ylabel('单价/元')
for i in range(len(type)):
    plt.scatter(data.loc[data['type'] == type[i],'total_price'],
                data.loc[data['type'] == type[i],'unit_price'],
                c = colors[i],label=str(type[i]))
plt.legend(loc='best')
plt.savefig('output/scatter',dpi = 300)

# bar
sec_name = data['区域'].unique()
section = []
for name in sec_name:
    section.append({
        'name':name,
        'total_price':np.mean(data.loc[data['区域'] == name,'total_price']),
        'unit_price':np.mean(data.loc[data['区域'] == name,'unit_price']),
        'nums':len(data.loc[data['区域'] == name]), 'x':0, 'width': 1
    })
section.sort(key=lambda x:x['nums'])
for i in range(1,len(section)):
    section[i]['width'] = section[0]['width'] * section[i]['nums'] / section[0]['nums']
    section[i]['x'] = section[i-1]['x']+section[i-1]['width']
for ele in ['unit_price','total_price']:
    colors = random_color(len(section) + 1)
    plt.figure()
    for i in range(0,len(section)):
        plt.bar(section[i]['x'],section[i][ele],width=section[i]['width'],label=str(section[i]['name'],align='edge',color=colors[i],alpha=0.8))
    plt.xlabel('楼盘数量/' + str(section[0]['nums'] / section[0]['width']) + '个')
    plt.ylabel('平均单价/元' if ele == 'unit_price' else '总价/万元')
    plt.legend(loc='best')
    plt.savefig('output/'+ ele,dpi = 300)

# to csv
data = data.sort_values(by='unit_price')
data.rename(columns={'name':'房名','type':'户型','room':'房型','area':'面积(平米)','unit_price':'均价(元)','total_price':'总价(万元)'},inplace=True) 
data.insert(2,'区域',data.pop('区域'))
data.insert(3,'位置',data.pop('位置'))
data.insert(4,'地点',data.pop('地点'))
data.to_csv('output/new_house.csv',index=None,encoding='utf_8_sig')
