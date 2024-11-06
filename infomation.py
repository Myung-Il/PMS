import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

inbutter_id = 1
t = {'월':7,'일':1,'시':23,'분':5}
# 현재 날짜가 아닌 경우에는 월-일 23:59 로 들어가게 설정

# 인버터 아이디에 맞는 파일 열고 시간을 코드가 사용할 수 있게 설정(여기까지가 준비과정)
df = pd.read_csv(f'./mokpo/info{inbutter_id}.csv',encoding='cp949')
df['측정일시'] = pd.to_datetime(df['측정일시'])
end_time = pd.to_datetime(f"2021-{t['월']}-{t['일']}  {t['시']}:{t['분']}:00")
start_time = pd.to_datetime(f"2021-{t['월']}-{t['일']}  23:59:00")-pd.Timedelta(days=1)

data = df.loc[(df['인버터아이디']==inbutter_id)&
                (df['측정일시']>start_time)&
                (df['측정일시']<=end_time)]

print(data)