import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# 장소별로 인버터 번호 할당
id_in_place = {"정선한교":[1],"함백태양광발전소":[6],"판교가압장 태양광발전소":[33,34],"서천태양광발전소":[4,5]}

# 화면에 띄울 인버터 아이디와 현재? 시간 설정
inbutter_id = 1
t = {'월':7,'일':20,'시':10,'분':5}

# 인버터 아이디에 맞는 파일 열고 시간을 코드가 사용할 수 있게 설정(여기까지가 준비과정)
df = pd.read_csv(f'./mokpo/info{inbutter_id}.csv',encoding='cp949')
df['측정일시'] = pd.to_datetime(df['측정일시'])
time = pd.to_datetime(f"2021-{t['월']}-{t['일']}  {t['시']}:{t['분']}:00")

########## 화면에 나올 부분을 자료에서 찾는 과정(현재 설정시간 1시간 전부터 설정 시간까지 나오게함)
data = df.loc[(df['인버터아이디']==inbutter_id)&
                (df['측정일시']>time-pd.Timedelta(hours=1))&
                (df['측정일시']<=time)]
data1 = data.loc[(df['측정일시']==time)]
# 시간을 보기 쉽게 설정
data['측정일시'] = data['측정일시'].dt.strftime("%H:%M")
data1['측정일시'] = data1['측정일시'].dt.strftime("%H:%M")

# 화면에 나올 y축을 정리할 때 사용할 변수 설정
maximum = max(data['유효전력(종합)'].max(),data['무효전력(종합)'].max())
maximum = maximum if maximum>10 else 10
ck = maximum//5

grid = gridspec.GridSpec(1,3)

# 화면에 어떻게 띄울건지 설정
plt.subplot(grid[0,:2]).plot(data['측정일시'],data['유효전력(종합)'],label='유효전력')
plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in plt.gca().get_yticks()])
plt.subplot(grid[0,:2]).plot(data['측정일시'],data['무효전력(종합)'],label='무효전력')
plt.yticks(np.arange(ck,maximum,ck))
plt.xticks(np.arange(0,60,10))
plt.legend()
plt.grid(True)
plt.subplot(grid[0,2]).bar(data1['측정일시'],data1['역률(종합)'])

# 그래프의 인터페이스를 설정 후 이미지파일 저장
plt.yticks(np.arange(0,100,10))
plt.show()