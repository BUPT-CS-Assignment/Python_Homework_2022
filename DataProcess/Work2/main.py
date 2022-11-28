import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('data/PEK.csv',encoding='utf-8')

# linear interpolation
for ele in ['HUMI','PRES','TEMP']:
    data[ele].interpolate()
    std = np.std(data[ele])
    data[ele].apply(lambda x: std * 3 if x > std else x)

# abnormal data process
for ele in ['PM_Dongsi','PM_Dongsihuan','PM_Nongzhanguan','PM_US Post']:
    data[ele] = data[ele].apply(lambda x:500 if x > 500 else -1 if np.isnan(x) else x).astype(int)

# back fill
data['cbwd'] = data['cbwd'].apply(lambda x:np.nan if x == 'cv' else x).bfill()

# storage
data.to_csv('output/PEK_fixed.csv')
        
# normalization and plot
def minmax(ele):
    return ((data[ele] - data[ele].min()) / (data[ele].max() - data[ele].min())).round(decimals=2)
def standard(ele):
    return ((data[ele] - data[ele].mean()) / data[ele].std()).round(decimals=2)

fig,pic = plt.subplots(figsize=(10,4),nrows = 1, ncols = 3)
sca_data = {
    'Original':{'pos':0,'DEWP':data['DEWP'],'TEMP':data['TEMP']},
    'MinMaxScaler':{'pos':1,'DEWP':minmax('DEWP'),'TEMP':minmax('TEMP')},
    'StandardScaler':{'pos':2,'DEWP':standard('DEWP'),'TEMP':standard('TEMP')}
}
for key in sca_data:
    node = sca_data[key]
    pic[node['pos']].set(title=key)
    pic[node['pos']].scatter(node['TEMP'], node['DEWP'])
    pic[node['pos']].grid(True, linestyle='--', alpha = 0.8)
pic[0].set_xlabel('TEMP', weight = 'bold')
pic[0].set_ylabel('DEWP', weight = 'bold')
plt.savefig('output/scatter')

# process PM
PM = []
for i in range(len(data)):
    pms = []
    [pms.append(data[pos][i]) if data[pos][i] != -1 else None for pos in ['PM_Dongsi','PM_Dongsihuan','PM_Nongzhanguan','PM_US Post']]
    PM.append(int(np.mean(pms)) if len(pms) > 2  else int(np.max(pms)) if len(pms) > 0 else -1)
    
# discretization and count
sec = [0,50,100,150,200,300,9999]
sec_type=['优','良','轻度污染','中度污染','重度污染','严重污染']
with open('output/PM.out','w') as f:
    f.write('[PM RESULT]\n')
    f.write(str(pd.value_counts(pd.cut(PM,sec,labels=sec_type))) + '\n')
    f.close()