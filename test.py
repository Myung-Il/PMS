import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.gridspec as gridspec

# [기본 설정]
# 폰트가 안깨지게 해주는 부분
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

options = {"정선한교":[1],
            "함백태양광발전소":[6],
            "판교가압장 태양광발전소":[33,34],
            "서천태양광발전소":[4,5]}
inbutter_id = 1
df = pd.read_csv(f'./mokpo/info{inbutter_id}.csv',encoding='cp949')
df['측정일시'] = pd.to_datetime(df['측정일시'])

t = {'월':7,'일':1,'시':7,'분':5}
time = pd.to_datetime(f"2021-{t['월']}-{t['일']}  {t['시']}:{t['분']}:00")

data = df.loc[(df['인버터아이디']==inbutter_id)&
              (df['측정일시']==time)]

# [현황]
# 이거 float인데 소수점 2번째까지만 나오게해서 넣자
print("인버팅후 인버터전력 :", data["인버팅후 인버터전력"].to_list()[0])
print("인버팅후 금일발전량 :", data["인버팅후 금일발전량"].tolist())
print("인버팅후 누적발전량 :", data["인버팅후 누적발전량"])

print("외부온도(인버터단위) :", data["외부온도(인버터단위)"])
print("모듈온도(인버터단위) :", data["모듈온도(인버터단위)"])

# [인버터 관리]
data = df.loc[(df['인버터아이디']==inbutter_id)&
              (df['측정일시']>=time-pd.Timedelta(hours=1))&
              (df['측정일시']<time)]

# 시간을 보기 쉽게 설정
data['측정일시'] = data['측정일시'].dt.strftime("%H:%M")

# 화면에 나올 y축을 정리할 때 사용할 변수 설정
maximum = max(data['인버터전류(R상)'].max(),data['인버터전류(S상)'].max(),data['인버터전류(T상)'].max())
maximum = maximum if maximum>10 else 10
ck = maximum//5

# 화면에 어떻게 띄울건지 설정(전류, 전압, 주파수 순서)
data.plot.line(x='측정일시',y=['인버터전류(R상)','인버터전류(S상)','인버터전류(T상)'],title='인버터전류')
data.plot.line(x='측정일시',y=['인버터전압(R상)','인버터전압(S상)','인버터전압(T상)'],title='인버터전압')
data.plot.line(x='측정일시',y=['인버터주파수'],title='인버터주파수')

# 그래프의 인터페이스를 설정 후 이미지파일 저장
plt.yticks(np.arange(ck,maximum,ck))
plt.grid(True)
plt.legend(loc='right')
# 파일 이름은 알아서
plt.savefig("plot.png")

# [발전] ey.py에서 #으로 표시해둔 부분부터 보세요
data = df.loc[(df['인버터아이디']==inbutter_id)&
              (df['측정일시']>time-pd.Timedelta(hours=1))&
              (df['측정일시']<=time)]


# 시간을 보기 쉽게 설정
data['측정일시'] = data['측정일시'].dt.strftime("%H:%M")

grid = gridspec.GridSpec(3,1)

# 화면에 나올 y축을 정리할 때 사용할 변수 설정
name_list = ["인버팅전 모듈전력(PV)","인버팅전 모듈전압(PV)","인버팅전 모듈전류(PV)"]
maximum_list = [data[name].max() for name in name_list]
for i in range(3):maximum_list[i] = maximum_list[i] if maximum_list[i]>10 else 10
ck_list = [i//5 for i in maximum_list]

# 화면에 어떻게 띄울건지 설정(전류, 전압, 주파수 순서)
for i in range(3):
    plt.subplot(grid[i,0]).plot(data['측정일시'],data[name_list[i]],label=name_list[i][:-4])
    plt.yticks(np.arange(ck_list[i],maximum_list[i],ck_list[i]))
    plt.grid(True)
    plt.legend(loc='right')
# 파일 이름은 알아서
plt.savefig("plot.png")

