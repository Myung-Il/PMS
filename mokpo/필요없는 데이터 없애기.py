import pandas as pd

# 안쓰는 발전소에대한 정보 삭제
data = pd.read_csv(f'info_com.csv',encoding='UTF-8')

name = ["정선한교","함백태양광발전소","판교가압장 태양광발전소","서천태양광발전소"]
idx = set(data.index)
for i in name:
    idx -= set(data.loc[data['장소']==i].index)
data.drop(idx,inplace=True)
data.to_csv("./info.csv",encoding='cp949')