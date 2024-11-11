from tkinter import ttk
import tkinter as tk
import tkinter.font
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image, ImageTk
Image.ANTIALIAS = Image.LANCZOS

# [ 변수 ]
# 메인
window = tk.Tk()
month, day, hour, minute = 7, 10, 7, 5

# 창 사이즈
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# tk 노트북
s = ttk.Style()
s.configure('TNotebook', tabposition='ne')
notebook = ttk.Notebook(window, width=1280, height=900)
notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=40)
style = ttk.Style()
style.configure("TNotebook.Tab", padding=[20, 10])

# 라벨 설정
frame_label = ["현황", "인버터 관리", "발전", "정보", "진단"]
frame_dict = {elm:tk.Frame(notebook) for elm in frame_label}

# 캔버스
canvas_dict = {elm:tk.Canvas(frame_dict[elm], bg="white") for elm in frame_label}
for elm in canvas_dict.values(): elm.pack(expand=True, fill='both')

# 추가할 라디오 버튼 옵션 (발전 관련 정보)
radio_gen_var1 = tk.IntVar(value=1)
radio_gen_var2 = tk.IntVar(value=1)
menu_visible = False

# 콤보박스에 들어갈 옵션 목록
options = {"정선한교(1)":1, 
        "함백태양광발전소(6)":6, 
        "판교가압장 태양광발전소(33)":33, "판교가압장 태양광발전소(34)":34, 
        "서천태양광발전소(4)":4, "서천태양광발전소(5)":5}
options_name = list(options.keys())



# [ 함수 ]
def time_control():
    global month, day, hour, minute
    minute += 1
    if minute==60: hour, minute =  hour+1, 0
    if   hour==60:  day,   hour =   day+1, 0
    if  day==31 and month in [7, 8, 10]: month, day = month+1, 0
    if  day==30 and month in [    9   ]: month, day = month+1, 0

    plt.clf()
    draw_quadrant_rectangles()
    img_create(notebook.tab(notebook.select(), "text"))
    window.update()

    lbl.config(text=f"2021년{month:>3d}월{day:>3d}일 {hour:0>2d}:{minute:0>2d}")
    window.after(1000, time_control)
    
# 화면 구성
# 발전 탭의 메뉴 숨기기/나타내기 버튼 생성
def toggle_menu_generation(toggle, box, List, lenght):
    global menu_visible

    if menu_visible and toggle['text']=="메뉴 나타내기":
        box.place(x=10, y=50)  # 체크박스를 나타냄
        toggle.config(text="메뉴 숨기기")
        box.tkraise()
        # 체크박스 및 라디오 버튼 배치
        for idx in range(lenght):List[idx].pack(anchor="w")

    elif not menu_visible and toggle['text']=="메뉴 숨기기":
        box.place_forget()  # 체크박스를 숨김
        toggle.config(text="메뉴 나타내기")

    elif not menu_visible:
        box.place(x=10, y=50)  # 체크박스를 나타냄
        toggle.config(text="메뉴 숨기기")
        box.tkraise()
        # 체크박스 및 라디오 버튼 배치
        for idx in range(lenght):List[idx].pack(anchor="w")

    elif menu_visible:
        box.place_forget()  # 체크박스를 숨김
        toggle.config(text="메뉴 나타내기")
        
    menu_visible = not menu_visible

def on_img(canvas, img): # 이미지를 띄우는 함수
        canvas.delete("all")   # 기존 이미지 지우기
        img = Image.open(img)         # 보여줄 이미지 설정

        img_width, img_height = img.size           # 이미지 크기
        width, height = canvas.winfo_width(), canvas.winfo_height()
        ratio = min(width/img_width, height/img_height) # 캔버스의 크기를 고려해서 조절
        img = img.resize((int(img_width * ratio), int(img_height * ratio)), Image.ANTIALIAS) # 이미지 크기 변경

        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(width/2, height/2, anchor=tk.CENTER, image=img_tk)
        canvas.img = img_tk

def img_create(title):
    if title=="인버터 관리":
        inverter_graph(options[combo.get()], radio_gen_var1.get())
        on_img(canvas_dict[title], "inverter_plot.png")
    if title=="발전":
        development_graph(options[combo.get()], radio_gen_var2.get())
        on_img(canvas_dict[title], "develop_plot.png")


# [ 현황 ]
# 화면 구성
def draw_quadrant_rectangles():
    width = canvas_dict["현황"].winfo_width()   # 창 너비 끝
    height = canvas_dict["현황"].winfo_height() # 창 높이 끝
    width_2_1 = width*2/3          # 두 캔버스 중앙
    height_half = height/2         # 높이 중앙
    height_1_3 = height/3          # 1 : 1 : 1

    # 기존 사각형 제거 후 다시 그리기
    canvas_dict["현황"].delete("all")
    ip, deg, cpg, et, mt = current_situation(options[combo.get()])

    # 왼 (상, 중, 하)
    canvas_dict["현황"].create_rectangle(0,            0, width_2_1,   height_1_3, fill="lightblue")
    canvas_dict["현황"].create_text(width_2_1/2, height_1_3/2, text=f"{ip} W", fill='black', font=font)

    canvas_dict["현황"].create_rectangle(0,   height_1_3, width_2_1, height_1_3*2, fill="lightgreen")
    canvas_dict["현황"].create_text(width_2_1/2, height_1_3*3/2, text=f"{deg} Wh", fill='black', font=font)

    canvas_dict["현황"].create_rectangle(0, height_1_3*2, width_2_1,       height, fill="lightcoral")
    canvas_dict["현황"].create_text(width_2_1/2, height*5/6, text=f"{cpg} Wh", fill='black', font=font)
    

    # 오 (상 하)
    canvas_dict["현황"].create_rectangle(width_2_1,           0, width, height_half, fill="#6495ED")
    canvas_dict["현황"].create_text(width*5/6, height/4, text=f"{et} ºC", fill='black', font=font)

    canvas_dict["현황"].create_rectangle(width_2_1, height_half, width,      height, fill="#E0FFFF")
    canvas_dict["현황"].create_text(width*5/6, height*3/4, text=f"{mt} ºC", fill='black', font=font)

def current_situation(inverter_id):
    global month, day, hour, minute

    # [기본 설정]
    # 폰트가 안깨지게 해주는 부분
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False

    df = pd.read_csv(f'./info{inverter_id}.csv',encoding='cp949')
    df['측정일시'] = pd.to_datetime(df['측정일시'])
    time = pd.to_datetime(f"2021-{month}-{day}  {hour}:{minute}:00")

    data = df.loc[(df['인버터아이디']==inverter_id)&
                (df['측정일시']==time)]

    # [현황]
    # 이거 float인데 소수점 2번째까지만 나오게해서 넣자
    inverter_power = f"인버팅후 인버터전력 : {data['인버팅후 인버터전력'].to_list()[0]:.2f}"
    day_electricity_generation = f"인버팅후 금일발전량 : {data['인버팅후 금일발전량'].to_list()[0]:.2f}"
    cumulative_power_generation = f"인버팅후 누적발전량 : {data['인버팅후 누적발전량'].to_list()[0]:.2f}"

    external_temperature = f"외부온도(인버터단위) : {data['외부온도(인버터단위)'].to_list()[0]:.2f}"
    module_temperature = f"모듈온도(인버터단위) : {data['모듈온도(인버터단위)'].to_list()[0]:.2f}"

    return inverter_power, day_electricity_generation, cumulative_power_generation, external_temperature, module_temperature


# [ 인버터 관리 ]
def inverter_graph(inverter_id,radio_btn_num):
    global month, day, hour, minute

    # [기본 설정]
    # 폰트가 안깨지게 해주는 부분
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False

    df = pd.read_csv(f'./info{inverter_id}.csv',encoding='cp949')
    df['측정일시'] = pd.to_datetime(df['측정일시'])
    time = pd.to_datetime(f"2021-{month}-{day}  {hour}:{minute}:00")
    data = df.loc[(df['인버터아이디']==inverter_id)&
              (df['측정일시']>=time-pd.Timedelta(hours=1))&
              (df['측정일시']<=time)]

    # 시간을 보기 쉽게 설정
    data['측정일시'] = data['측정일시'].dt.strftime("%H:%M")

    # 화면에 어떻게 띄울건지 설정(전류, 전압, 주파수 순서)
    if radio_btn_num == 1:
        data.plot.line(x='측정일시',y=['인버터전압(R상)','인버터전압(S상)','인버터전압(T상)'],title='인버터전압 (V)')
        # 화면에 나올 y축을 정리할 때 사용할 변수 설정
        maximum = max(data['인버터전압(R상)'].max(),data['인버터전압(S상)'].max(),data['인버터전압(T상)'].max())
        maximum = maximum if maximum>10 else 10
        ck = maximum//5
        plt.yticks(np.arange(ck,maximum+2,ck))
    elif radio_btn_num == 2:
        data.plot.line(x='측정일시',y=['인버터전류(R상)','인버터전류(S상)','인버터전류(T상)'],title='인버터전류 (A)')
        maximum = max(data['인버터전류(R상)'].max(),data['인버터전류(S상)'].max(),data['인버터전류(T상)'].max())
        maximum = maximum if maximum>10 else 10
        ck = maximum//5
        plt.yticks(np.arange(ck,maximum+2,ck))
    elif radio_btn_num == 3:
        print(data.loc[data["측정일시"]==time]['인버터주파수'])
        data.plot.line(x='측정일시',y='인버터주파수',title='인버터주파수 (Hz)')
        plt.yticks(np.arange(0,102,20))
    else:
        plt.text("인버터 그래프 오류 발생")

    # 그래프의 인터페이스를 설정 후 이미지파일 저장
    plt.grid(True)
    plt.legend()
    # 파일 이름은 알아서
    plt.savefig("inverter_plot.png")

    width = canvas_dict["인버터 관리"].winfo_width()   # 창 너비 끝
    height = canvas_dict["인버터 관리"].winfo_height() # 창 높이 끝

    g = Image.open("./inverter_plot.png")
    g = g.resize((width,height), Image.ANTIALIAS)
    g = ImageTk.PhotoImage(g)
    canvas_dict["인버터 관리"].create_image(0, 0, image=g)

# [ 발전 ]
def development_graph(inverter_id,radio_btn_num):
    global month, day, hour, minute

    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False

    df = pd.read_csv(f'./info{inverter_id}.csv',encoding='cp949')
    df['측정일시'] = pd.to_datetime(df['측정일시'])
    time = pd.to_datetime(f"2021-{month}-{day}  {hour}:{minute}:00")

    ########## 화면에 나올 부분을 자료에서 찾는 과정(현재 설정시간 1시간 전부터 설정 시간까지 나오게함)
    data = df.loc[(df['인버터아이디']==inverter_id)&
                    (df['측정일시']>=time-pd.Timedelta(hours=1))&
                    (df['측정일시']<=time)]
    data1 = data.loc[(df['측정일시']==time)]
    # 시간을 보기 쉽게 설정
    data['측정일시'] = data['측정일시'].dt.strftime("%H:%M")
    data1['측정일시'] = data1['측정일시'].dt.strftime("%H:%M")

    if radio_btn_num == 1:
        # 화면에 나올 y축을 정리할 때 사용할 변수 설정
        maximum = max(data['유효전력(종합)'].max(),data['무효전력(종합)'].max())
        maximum = maximum if maximum>10 else 10
        ck = maximum//5

        grid = gridspec.GridSpec(1,3,wspace=0.3,hspace=0.3)

        # 화면에 어떻게 띄울건지 설정
        plt.subplot(grid[0,:2]).plot(data['측정일시'],data['유효전력(종합)'],label='유효전력')
        plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in plt.gca().get_yticks()])
        plt.subplot(grid[0,:2]).plot(data['측정일시'],data['무효전력(종합)'],label='무효전력')
        plt.yticks(np.arange(ck,maximum+2,ck))
        plt.xticks(np.arange(0,60,10))
        plt.legend()
        plt.grid(True)
        plt.subplot(grid[0,2]).bar(data1['측정일시'],data1['역률(종합)'],label='역률')
        plt.legend()
        plt.yticks(np.arange(0,102,10))

    elif radio_btn_num == 2:
        grid = gridspec.GridSpec(3,1,wspace=0.3,hspace=0.3)

        # 화면에 나올 y축을 정리할 때 사용할 변수 설정
        name_list = ["인버팅전 모듈전력(PV)","인버팅전 모듈전압(PV)","인버팅전 모듈전류(PV)"]
        maximum_list = [data[name].max() if data[name].max()>10 else 10 for name in name_list]
        ck_list = [i//5 for i in maximum_list]

        # 화면에 어떻게 띄울건지 설정(전류, 전압, 주파수 순서)
        for i in range(3):
            plt.subplot(grid[i,0]).plot(data['측정일시'],data[name_list[i]],label=name_list[i][:-4])
            plt.yticks(np.arange(ck_list[i],maximum_list[i]+2,ck_list[i]))
            plt.xticks(np.arange(0,60,10))
            plt.grid(True)
            plt.legend()
        # 파일 이름은 알아서

    else:
        plt.text("발전 그래프 오류 발생")

    width = canvas_dict["발전"].winfo_width()   # 창 너비 끝
    height = canvas_dict["발전"].winfo_height() # 창 높이 끝

    plt.savefig("develop_plot.png")

    g = Image.open("./develop_plot.png")
    g = g.resize((width,height), Image.ANTIALIAS)
    g = ImageTk.PhotoImage(g)
    canvas_dict["발전"].create_image(0, 0, image=g)


# [ 정보 ]


# [ 진단 ]




# [ 창 기능 ]
if __name__=="__main__":

    window.title("태양모니터링시스템")
    window.geometry(f"{screen_width}x{screen_height}")
    window.resizable(1, 1)

    font=tkinter.font.Font(family="맑은 고딕", size=18, slant="italic")

    # 가본 세팅
    combo = ttk.Combobox(window, values=options_name, font= font)
    combo = ttk.Combobox(window, values=options_name, width=20, style="TCombobox", font= font)  # width를 사용해 텍스트 영역 크기 설정
    combo.set("정선한교(1)")
    combo.place(x=150, y=0, anchor="n")

    # 현황

    # 인버터 관리
    # 메뉴 숨기기/나타내기 버튼 및 체크박스 프레임 생성
    toggle_btn_inverter = tk.Button(frame_dict["인버터 관리"], text="메뉴 나타내기")
    toggle_btn_inverter.place(x=10, y=10)

    box_frame_inverter = tk.LabelFrame(frame_dict["인버터 관리"], text="발전 메뉴", padx=10, pady=10)
    box_frame_inverter.place(x=10, y=70)

    radio_btn_inverter_list = [tk.Radiobutton(box_frame_inverter, text=elm, variable=radio_gen_var1, value=idx,
                                              command=lambda:img_create("인버터 관리"))
                               for elm, idx in [["전압", 1], ["전류", 2], ["주파수", 3]]]
    toggle_btn_inverter.config(command=lambda:toggle_menu_generation(toggle_btn_inverter, box_frame_inverter, radio_btn_inverter_list, 3))

    # 발전
    # 메뉴 숨기기/나타내기 버튼 및 체크박스 프레임 생성
    toggle_btn_develop = tk.Button(frame_dict["발전"], text="메뉴 나타내기")
    toggle_btn_develop.place(x=10, y=10)
    box_frame_develop = tk.LabelFrame(frame_dict["발전"], text="발전 메뉴", padx=10, pady=10)
    box_frame_develop.place(x=10, y=70)

    radio_btn_develop_list = [tk.Radiobutton(box_frame_develop, text=elm, variable=radio_gen_var2, value=idx,
                                              command=lambda:img_create("발전"))
                               for elm, idx in [["종합 전력", 1], ["인버팅 전", 2]]]
    toggle_btn_develop.config(command=lambda:toggle_menu_generation(toggle_btn_develop, box_frame_develop, radio_btn_develop_list, 2))


    # 기능
    window.after(1000, time_control)
    for name, frame in frame_dict.items(): notebook.add(frame, text=name)
    canvas_dict["현황"].bind("<Configure>", lambda event:draw_quadrant_rectangles())
    canvas_dict["인버터 관리"].bind("<Configure>", lambda event:img_create("인버터 관리"))
    radio_btn_inverter_list[0].select()
    canvas_dict["발전"].bind("<Configure>", lambda event:img_create("발전"))
    radio_btn_develop_list[0].select()

    lbl = tk.Label(window, font=font, text=f"2021년{month:>3d}월{day:>3d}일 {hour:0>2d}:{minute:0>2d}")
    lbl.place(x=300, y=0)

    #
    window.mainloop()