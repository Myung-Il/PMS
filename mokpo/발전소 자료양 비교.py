import pandas as pd

df = []
for i in ['07','08','09','10']:
    df.append(pd.read_csv(f'info_2021{i}.csv',encoding='cp949'))
    
data_place = {}

for i in df:
    data_place.update({j:[0] for j in set(i['장소'].values.tolist())})

for v in data_place.keys():
    for i in df:
        data_place[v][0] += len(i[i['장소'] == v])

data_place = dict(sorted(data_place.items(), key=lambda x: x[1][0], reverse=True))

print(data_place)