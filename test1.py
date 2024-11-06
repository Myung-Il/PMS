import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

# 폰트가 안깨지게 해주는 부분
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# 장소별로 인버터 번호 할당
id_in_place = {"정선한교":[1],"함백태양광발전소":[6],"판교가압장 태양광발전소":[33,34],"서천태양광발전소":[4,5]}

# 화면에 띄울 인버터 아이디와 현재? 시간 설정
inbutter_id = 1
t = {'월':7,'일':1,'시':7,'분':5}

# 인버터 아이디에 맞는 파일 열고 시간을 코드가 사용할 수 있게 설정(여기까지가 준비과정)
data = pd.read_csv(f'./mokpo/info{inbutter_id}.csv',encoding='cp949')
data['측정일시'] = pd.to_datetime(data['측정일시'])
time = pd.to_datetime(f"2021-{t['월']}-{t['일']}  {t['시']}:{t['분']}:00")

# 화면에 나올 부분을 자료에서 찾는 과정(현재 설정시간 1시간 전부터 설정 시간까지 나오게함)
test = data.loc[(data['인버터아이디']==inbutter_id)&
                (data['측정일시']>time-pd.Timedelta(hours=1))&
                (data['측정일시']<=time)]
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

# 그래프의 인터페이스를 설정 후 이미지파일 저장
plt.show()
# plt.savefig("plot.png")