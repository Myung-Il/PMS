import pandas as pd
import numpy as np

# 측정하는 시간을 분단위로 설정하여 데이터 프레임 생성
data = pd.read_csv('info.csv',encoding='cp949')
time = pd.date_range(start="2021-07-01  00:00:00", end="2021-10-30  23:59:00",freq='min').to_list()
time = pd.DataFrame({"측정일시":time})
place_id = [1,6,33,34,4,5]

# left join을 위해 각 데이터 프레임의 데이터 타입을 통일
data['측정일시'] = pd.to_datetime(data['측정일시'])
time['측정일시'] = pd.to_datetime(time['측정일시'])

# 각 인버터별로 조인 후 결측값을 앞 시간과 같은 값을 넣어주는 방식으로 처리하여 cvs파일로 저장
test = {}
for id in place_id:
        ck = pd.merge(time ,data.loc[data["인버터아이디"]==id], how = "left", left_on="측정일시", right_on="측정일시")
        ck = ck.interpolate(method='pad')
        test[id]=ck

for id in place_id:
        test[id].to_csv(f"./info{id}.csv",encoding='cp949')