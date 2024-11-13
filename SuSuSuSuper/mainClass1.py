from tkinter import ttk
import tkinter as tk
import tkinter.font
import numpy as np
import pandas as pd
from tksheet import Sheet
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image, ImageTk
Image.ANTIALIAS = Image.LANCZOS






# [ 함수 ]
def time_control():
    global month, day, hour, minute
    minute += 1
    if minute==60: hour, minute =  hour+1, 0
    if   hour==60:  day,   hour =   day+1, 0
    if  day==31 and month in [7, 8, 10]: month, day = month+1, 0
    if  day==30 and month in [    9   ]: month, day = month+1, 0

    plt.clf()
    currentSituation.draw_quadrant_rectangles()
    select_graph(notebook.tab(notebook.select(), "text"))
    diagnosis.setting(options[combo.get()])

    lbl.config(text=f"2021년{month:>3d}월{day:>3d}일 {hour:0>2d}:{minute:0>2d}")
    window.after(1000, time_control)

def select_graph(now):
    match now:
        case "인버터 관리":inverterManagement.inverter_graph(options[combo.get()], radio_gen_var1.get())
        case "발전":development.development_graph(options[combo.get()], radio_gen_var2.get())

class Menu:
    def __init__(self, canvas, var, radioList):
        self.canvas = canvas
        self.var = var
        self.radioList = radioList

        self.toggle, self.box, self.radio = None, None, None
        self.check1, self.check2, self.check3 = None, None, None
        self.menu_visible = False
    
    def createRadioBox(self, function):
        self.toggle = tk.Button(self.canvas, width=30, height=30, bitmap="info")
        self.box = tk.LabelFrame(self.canvas, text="발전 메뉴", padx=10, pady=10)
        self.radio = [tk.Radiobutton(self.box, text=elm, variable=self.var, value=idx,
                                     command=lambda:function(options[combo.get()], self.var.get()))
                                     for elm, idx in self.radioList]
        self.toggle.place(x=10, y=10)
        self.box.place(x=10, y=70)
        self.toggle.config(command=lambda:self.generation(self.radio))

    def createCheckBox(self, function):
        self.toggle = tk.Button(self.canvas, width=30, height=30, bitmap="info")
        self.box = tk.LabelFrame(self.canvas, text="발전 메뉴", padx=10, pady=10)
        self.boxCanvas = tk.Canvas(self.box, width=100, height=10)
        self.check1 = [tk.Checkbutton(self.box, text=elm, variable=self.var[idx],
                                     command=lambda:function())
                                     for elm, idx in self.radioList[0]]
        self.check2 = [tk.Checkbutton(self.box, text=elm, variable=self.var[idx],
                                     command=lambda:function())
                                     for elm, idx in self.radioList[1]]
        self.check3 = [tk.Checkbutton(self.box, text=elm, variable=self.var[idx],
                                     command=lambda:function())
                                     for elm, idx in self.radioList[2]]
        self.toggle.place(x=10, y=10)
        self.box.place(x=10, y=70)
        self.toggle.config(command=lambda:self.generation(self.check1, self.check2, self.check3))

    def generation(self, List1, List2=[], List3=[]):
        if self.menu_visible:
            self.box.place_forget()
        else:
            self.box.place(x=10, y=50)
            self.box.tkraise()
            self.line = None
            for elm in List1:elm.pack(anchor="w")
            for elm in List2:elm.pack(anchor="w")
            for elm in List3:elm.pack(anchor="w")
        self.menu_visible = not self.menu_visible

class Frame:
    def __init__(self, name):
        self.name = name
        self.frame = tk.Frame(notebook)
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(expand=True, fill='both')

    def on_graph(self, img):
        self.canvas.delete("all")
        img = Image.open(img)
        
        img_width, img_height = img.size
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        ratio = min(width/img_width, height/img_height)
        img = img.resize((int(img_width * ratio), int(img_height * ratio)), Image.ANTIALIAS)

        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(width/2, height/2, anchor=tk.CENTER, image=img_tk)
        self.canvas.img = img_tk

class CurrentSituation(Frame):
    def __init__(self):
        super().__init__("현황")

    def draw_quadrant_rectangles(self):
        width = self.canvas.winfo_width()   # 창 너비 끝
        height = self.canvas.winfo_height() # 창 높이 끝
        width_2_1 = width*2/3          # 두 캔버스 중앙
        height_half = height/2         # 높이 중앙
        height_1_3 = height/3          # 1 : 1 : 1

        # 기존 사각형 제거 후 다시 그리기
        self.canvas.delete("all")
        ip, deg, cpg, et, mt = self.current_situation(options[combo.get()])

        rectangle = [
            (        0,            0, width_2_1,   height_1_3,  "lightblue"),
            (        0,   height_1_3, width_2_1, height_1_3*2, "lightgreen"),
            (        0, height_1_3*2, width_2_1,       height, "lightcoral"),
            (width_2_1,            0,     width,  height_half,    "#6495ED"),
            (width_2_1,  height_half,     width,       height,    "#E0FFFF")
        ]
        text = [
            (width_2_1/2,   height_1_3/2,  ip,  "W"),
            (width_2_1/2, height_1_3*3/2, deg, "Wh"),
            (width_2_1/2,     height*5/6, cpg, "Wh"),
            (  width*5/6,       height/4, et,  "ºC"),
            (  width*5/6,     height*3/4, mt,  "ºC")
        ]
        
        for x1, y1, x2, y2, color in rectangle:self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        for x, y, data, unit in text:self.canvas.create_text(x, y, text=f"{data} {unit}", fill='black', font=font)

    def current_situation(self, id):
        global month, day, hour, minute
        
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False

        df = pd.read_csv(f'./info{id}.csv', encoding='cp949')
        df['측정일시'] = pd.to_datetime(df['측정일시'])
        time = pd.to_datetime(f"2021-{month}-{day} {hour}:{minute}:00")
        data = df[(df['인버터아이디'] == id) & (df['측정일시'] == time)].iloc[0]

        return (
            f"인버팅후 인버터전력 : {data['인버팅후 인버터전력']:.2f}",
            f"인버팅후 금일발전량 : {data['인버팅후 금일발전량']:.2f}",
            f"인버팅후 누적발전량 : {data['인버팅후 누적발전량']:.2f}",
            f"외부온도(인버터단위) : {data['외부온도(인버터단위)']:.2f}",
            f"모듈온도(인버터단위) : {data['모듈온도(인버터단위)']:.2f}"
        )

class InverterManagement(Frame, Menu):
    def __init__(self):
        Frame.__init__(self, "인버터 관리")
        Menu.__init__(self, self.canvas, radio_gen_var1, [["전압", 1], ["전류", 2], ["주파수", 3]])
        self.createRadioBox(self.inverter_graph)

    def inverter_graph(self, id, var):
        global month, day, hour, minute
        
        plt.rcParams['font.family'] ='Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] =False

        df = pd.read_csv(f'./info{id}.csv',encoding='cp949')
        df['측정일시'] = pd.to_datetime(df['측정일시'])
        time = pd.to_datetime(f"2021-{month}-{day}  {hour}:{minute}:00")

        data = df.loc[(df['인버터아이디']==id)&
                (df['측정일시']>=time-pd.Timedelta(hours=1))&
                (df['측정일시']<=time)]
        data['측정일시'] = data['측정일시'].dt.strftime("%H:%M")

        if var == 1:
            data.plot.line(x='측정일시',y=['인버터전압(R상)','인버터전압(S상)','인버터전압(T상)'],title='인버터전압 (V)')
            maximum = max(data['인버터전압(R상)'].max(),data['인버터전압(S상)'].max(),data['인버터전압(T상)'].max())
            maximum = maximum if maximum>10 else 10
            ck = maximum//5
            plt.yticks(np.arange(ck,maximum+2,ck))
        elif var == 2:
            data.plot.line(x='측정일시',y=['인버터전류(R상)','인버터전류(S상)','인버터전류(T상)'],title='인버터전류 (A)')
            maximum = max(data['인버터전류(R상)'].max(),data['인버터전류(S상)'].max(),data['인버터전류(T상)'].max())
            maximum = maximum if maximum>10 else 10
            ck = maximum//5
            plt.yticks(np.arange(ck,maximum+2,ck))
        elif var == 3:
            print(data.loc[data["측정일시"]==time]['인버터주파수'])
            data.plot.line(x='측정일시',y='인버터주파수',title='인버터주파수 (Hz)')
            plt.yticks(np.arange(0,102,20))
        else: plt.text("인버터 그래프 오류 발생")

        plt.grid(True)
        plt.legend()
        
        plt.savefig("inverter_plot.png")
        self.on_graph("./inverter_plot.png")

class Development(Frame, Menu):
    def __init__(self):
        Frame.__init__(self, "발전")
        Menu.__init__(self, self.canvas, radio_gen_var2, [["종합 전력", 1], ["인버팅 전", 2]])
        self.createRadioBox(self.development_graph)

    def development_graph(self, id, var):
        global month, day, hour, minute

        plt.rcParams['font.family'] ='Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] =False

        df = pd.read_csv(f'./info{id}.csv',encoding='cp949')
        df['측정일시'] = pd.to_datetime(df['측정일시'])
        time = pd.to_datetime(f"2021-{month}-{day}  {hour}:{minute}:00")

        data = df.loc[(df['인버터아이디']==id) &
                        (df['측정일시']>=time-pd.Timedelta(hours=1))&
                        (df['측정일시']<=time)]
        data1 = data.loc[(df['측정일시']==time)]
        data['측정일시'] = data['측정일시'].dt.strftime("%H:%M")
        data1['측정일시'] = data1['측정일시'].dt.strftime("%H:%M")

        if var == 1:
            maximum = max(data['유효전력(종합)'].max(),data['무효전력(종합)'].max())
            maximum = maximum if maximum>10 else 10
            ck = maximum//5

            grid = gridspec.GridSpec(1,3,wspace=0.3,hspace=0.3)
            plt.subplot(grid[0,:2]).plot(data['측정일시'],data['유효전력(종합)'],label='유효전력')
            plt.subplot(grid[0,:2]).plot(data['측정일시'],data['무효전력(종합)'],label='무효전력')
            plt.yticks(np.arange(ck,maximum+2,ck))
            plt.xticks(np.arange(0,60,10))
            plt.legend()
            plt.grid(True)
            plt.subplot(grid[0,2]).bar(data1['측정일시'],data1['역률(종합)'],label='역률')
            plt.legend()
            plt.yticks(np.arange(0,102,10))

        elif var == 2:
            grid = gridspec.GridSpec(3,1,wspace=0.3,hspace=0.3)
            name_list = ["인버팅전 모듈전력(PV)","인버팅전 모듈전압(PV)","인버팅전 모듈전류(PV)"]
            maximum_list = [data[name].max() if data[name].max()>10 else 10 for name in name_list]
            ck_list = [i//5 for i in maximum_list]

            for i in range(3):
                plt.subplot(grid[i,0]).plot(data['측정일시'],data[name_list[i]],label=name_list[i][:-4])
                plt.yticks(np.arange(ck_list[i],maximum_list[i]+2,ck_list[i]))
                plt.xticks(np.arange(0,60,10))
                plt.grid(True)
                plt.legend()
        else: plt.text("발전 그래프 오류 발생")

        plt.savefig("develop_plot.png")
        self.on_graph("./develop_plot.png")

class Information(Frame, Menu):
    def __init__(self):
        self.info = [[["전압", 0], ["전류", 1], ["주파수", 2]],
                     [["종합 전력", 3], ["인버팅 전 전력", 4], ["인버팅 전 전압", 5], ["인버팅 전 전류", 6]],
                     [["인버팅 후 발전량", 7], ["온도", 8]]]
        Frame.__init__(self, "정보")
        Menu.__init__(self, self.canvas, check_gen_varList, self.info)
        self.getDataItems = []
        self.c = {"전압":["인버터전압(R상)","인버터전압(S상)","인버터전압(T상)"],"전류":["인버터전류(R상)","인버터전류(S상)","인버터전류(T상)"],"주파수":["인버터주파수"],
                    "종합 전력":["유효전력(종합)","무효전력(종합)","역률(종합)"],"인버팅 전 전력":["인버팅전 모듈전력(PV)"],"인버팅 전 전압":["인버팅전 모듈전압(PV)"],"인버팅 전 전류":["인버팅전 모듈전류(PV)"],
                    "인버팅 후 발전량":["인버팅후 누적발전량","인버팅후 금일발전량"],"온도":["외부온도(인버터단위)","모듈온도(인버터단위)"]}
        self.createCheckBox(self.getData)

        self.canvas.bind("<Configure>", self.update_button_positions)
        self.yearComboBox = ttk.Combobox(self.canvas, values=[2021], width=10, font=("맑은 고딕", 16))
        self.yearLabel = tk.Label(self.canvas, font=("맑은 고딕", 10), text="년도")
        self.yearComboBox.set(2021)
        
        self.monthComboBox = ttk.Combobox(self.canvas, values=list(range(7, 11)), width=10, font=("맑은 고딕", 16))
        self.monthLabel = tk.Label(self.canvas, font=("맑은 고딕", 10), text="월")
        self.monthComboBox.set(7)
        self.monthComboBox.bind("<<ComboboxSelected>>", self.update_day)

        self.dayComboBox = ttk.Combobox(self.canvas, width=10, font=("맑은 고딕", 16))
        self.dayLabel = tk.Label(self.canvas, font=("맑은 고딕", 10), text="일")
        self.update_day()
        self.dayComboBox.set(1)

        self.searchBtn = tk.Button(self.canvas, width=10, font=("맑은 고딕", 12), text="검색", command=lambda:self.search(options[combo.get()]))
        self.saveBtn = tk.Button(self.canvas, width=10, font=("맑은 고딕", 12), text="저장",  command=lambda:self.saveCSV(options[combo.get()]))

    def update_day(self, event=None):
        days = list(range(1, 31 + (1 if int(self.monthComboBox.get()) != 9 else 0)))
        self.dayComboBox['values'] = days

    def update_button_positions(self, event=None):
        width = self.canvas.winfo_width()
        self.yearComboBox.place(x=width-690, y=10)
        self.monthComboBox.place(x=width-535, y=10)
        self.dayComboBox.place(x=width-380, y=10)

        self.yearLabel.place(x=width-690, y=50)
        self.monthLabel.place(x=width-535, y=50)
        self.dayLabel.place(x=width-380, y=50)

        self.searchBtn.place(x=width - 225, y=10)
        self.saveBtn.place(x=width - 115, y=10)

    def getData(self):
        self.getDataItems = [elm for elmList in self.info for elm, idx in elmList if check_gen_varList[idx].get()]

    def search(self, id):
        self.chart(id)

    def saveCSV(self, id):
        time = pd.to_datetime(f"{self.yearComboBox.get()}-{self.monthComboBox.get()}-{self.dayComboBox.get()} 00:00:00")
        items = ['장소','측정일시']
        for i in self.getDataItems:
            items+=self.c[i]
        save_data = self.df.loc[(self.df["측정일시"]>=time)&(self.df["측정일시"]<time+pd.Timedelta(days=1)),items]
        save_data.to_csv(f"info_{id}_save.csv")

    def chart(self, id):
        self.df = pd.read_csv(f'./info{id}.csv',encoding='cp949')
        self.df['측정일시'] = pd.to_datetime(self.df['측정일시'])
        time = pd.to_datetime(f"{self.yearComboBox.get()}-{self.monthComboBox.get()}-{self.dayComboBox.get()} 00:00:00")
        items = ['측정일시']
        for i in self.getDataItems:
            items+=self.c[i]
        print_data = self.df.loc[(self.df["측정일시"]>=time)&(self.df["측정일시"]<time+pd.Timedelta(days=1)),items]
        print_data['측정일시'] = print_data['측정일시'].dt.strftime("%H:%M")

        sheet = Sheet(self.canvas, data=print_data.values.tolist())  # Convert DataFrame to list of lists for tksheet
        sheet.headers(print_data.columns.tolist())  # Set headers to column names
        sheet.height_and_width(height=600,width=1200)
        sheet.place(x=160, y=70)


class Diagnosis(Frame):
    def __init__(self):
        super().__init__("진단")

    def setting(self, id):
        global month, day, hour, minute
        
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False

        df = pd.read_csv(f'./info{id}.csv', encoding='cp949')
        df['측정일시'] = pd.to_datetime(df['측정일시'])
        time = pd.to_datetime(f"2021-{month}-{day} {hour}:{minute}:00")
        data = df[(df['인버터아이디'] == id) & (df['측정일시'] == time)]

        et = tk.Label(self.canvas, font=('맑은 고딕', 20))
        mt = tk.Label(self.canvas, font=('맑은 고딕', 20))
        pf = tk.Label(self.canvas, font=('맑은 고딕', 20))
        
        if data.loc[data['외부온도(인버터단위)']>=40].empty:et['text'] = '외부온도 이상무'
        else:et['text'] = '외부 온도가 너무 높습니다. 주의해주시기 바랍니다.'
        if data.loc[data['모듈온도(인버터단위)']>=60].empty:mt['text'] = '모듈온도 이상무'
        else:mt['text'] = '모듈 온도가 너무 높습니다. 인버터의 쿨러를 확인하여 주시기 바랍니다.'
        if data.loc[data['역률(종합)']<= 95].empty:pf['text'] = '역률 이상무'
        else:pf['text'] = '역률이 너무 낮습니다. 발전기를 확인하여주시기 바랍니다.'

        et.place(x=50, y=50)
        mt.place(x=50, y=250)
        pf.place(x=50, y=450)



if '__main__' == __name__:

    # window 설정
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.title("태양모니터링시스템")
    window.geometry(f"{screen_width}x{screen_height}")
    window.resizable(1, 1)

    # notebook 설정
    s = ttk.Style()
    s.configure('TNotebook', tabposition='ne')
    notebook = ttk.Notebook(window, width=1280, height=900)
    notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=40)
    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=[20, 10])

    # 변수
    month, day, hour, minute = 7, 10, 7, 5
    font=tkinter.font.Font(family="맑은 고딕", size=18, slant="italic")
    radio_gen_var1 = tk.IntVar(value=1)
    radio_gen_var2 = tk.IntVar(value=1)
    check_gen_varList = [tk.IntVar() for _ in range(9)]
    
    # 지역 설정
    options = {"정선한교(1)":1, 
            "함백태양광발전소(6)":6, 
            "판교가압장 태양광발전소(33)":33, "판교가압장 태양광발전소(34)":34, 
            "서천태양광발전소(4)":4, "서천태양광발전소(5)":5}
    options_name = list(options.keys())
    combo = ttk.Combobox(window, values=options_name, width=20, style="TCombobox", font= font)
    combo.set("정선한교(1)")
    combo.place(x=150, y=0, anchor="n")

    
    # [ 현황 ]
    currentSituation = CurrentSituation()
    notebook.add(currentSituation.frame, text=currentSituation.name)
    currentSituation.canvas.bind("<Configure>", lambda event:currentSituation.draw_quadrant_rectangles())

    # [ 인버터 관리 ]
    inverterManagement = InverterManagement()
    notebook.add(inverterManagement.frame, text=inverterManagement.name)
    inverterManagement.canvas.bind("<Configure>", lambda event:inverterManagement.inverter_graph(1, 1))

    # [ 발전 ]
    development = Development()
    notebook.add(development.frame, text=development.name)
    development.canvas.bind("<Configure>", lambda event:development.development_graph(1, 1))

    # [ 정보 ]
    information = Information()
    notebook.add(information.frame, text=information.name)

    # [ 진단 ]
    diagnosis = Diagnosis()
    notebook.add(diagnosis.frame, text=diagnosis.name)
    diagnosis.canvas.bind("<Configure>", lambda event:diagnosis.setting(1))


    # 기능
    lbl = tk.Label(window, font=font, text=f"2021년{month:>3d}월{day:>3d}일 {hour:0>2d}:{minute:0>2d}")
    lbl.place(x=300, y=0)
    window.after(1000, time_control)
    window.mainloop()