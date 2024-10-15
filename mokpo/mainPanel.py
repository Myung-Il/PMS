import tkinter as tk  # tkinter 모듈을 tk라는 별칭으로 임포트
from tkinter import ttk  # ttk 모듈에서 Combobox를 사용하기 위해 임포트

# 메인 윈도우 생성
window = tk.Tk()
window.title("")

# 화면 해상도 가져오기
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# 창 모드에서 화면을 꽉 채우는 크기로 설정
window.geometry(f"{screen_width}x{screen_height}")

window.resizable(1, 1)

# 캔버스 생성
canvas = tk.Canvas(window, width=screen_width, height=screen_height, bg="white")
canvas.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

# 콤보박스에 들어갈 옵션 목록
options = ["Option 1", "Option 2", "Option 3", "Option 4"]

# 콤보박스 생성
combo = ttk.Combobox(window, values=options)
combo.set("장소")
combo.place(x=300, y=0, anchor="n")

# 콤보박스에서 선택된 값을 출력하는 함수 정의
def on_select(event):
    selected_option = combo.get()

combo.bind("<<ComboboxSelected>>", on_select)

# 체크박스 상태를 저장할 변수 생성
checkbox_var7 = tk.IntVar()

# 사각형 ID를 저장할 변수
rectangle_id1 = None
rectangle_id2 = None
rectangle_id3 = None  # 주파수를 위한 변수 추가
other_rectangle_ids = []  # 기타 사각형 ID를 저장할 리스트

# 기타 버튼 클릭 시 사각형 4개 생성 함수
# 사각형의 크기를 업데이트하는 함수
def resize_other_rectangles(event):
    canvas_width = event.width
    canvas_height = event.height
    rect_width = canvas_width / 4  # 창 크기에 따라 사각형 너비 동적 조정
    rect_height = 200  # 사각형 높이 고정
    spacing = 0

    # 기존 사각형 제거 후 다시 그리기
    for rect_id in other_rectangle_ids:
        canvas.delete(rect_id)
    other_rectangle_ids.clear()

    for i in range(4):
        x0 = 0 + (rect_width + spacing) * i
        y0 = canvas_height - rect_height  # 화면 하단에 맞추기
        x1 = x0 + rect_width
        y1 = y0 + rect_height
        rect_id = canvas.create_rectangle(x0, y0, x1, y1, fill="green")
        other_rectangle_ids.append(rect_id)

# 기타 체크박스에 따른 사각형 표시/숨김 함수
def toggle_other_rectangles():
    if checkbox_var7.get() == 1:  # 체크박스가 체크된 경우
        # 사각형 생성
        rect_width = canvas.winfo_width() / 4  # 창 너비에 맞춰 4등분
        rect_height = 200
        spacing = 0
        for i in range(4):
            x0 = 0 + (rect_width + spacing) * i
            y0 = canvas.winfo_height() - rect_height  # 화면 하단에 맞추기
            x1 = x0 + rect_width
            y1 = y0 + rect_height
            rect_id = canvas.create_rectangle(x0, y0, x1, y1, fill="green")
            other_rectangle_ids.append(rect_id)

        canvas.bind("<Configure>", resize_other_rectangles)  # 창 크기 조정 이벤트에 바인딩
    else:  # 체크박스가 해제된 경우
        for rect_id in other_rectangle_ids:
            canvas.delete(rect_id)
        other_rectangle_ids.clear()
        canvas.unbind("<Configure>")  # 크기 조정 이벤트 바인딩 해제

# 체크박스를 담을 LabelFrame 생성
checkbox_frame = tk.LabelFrame(window, text="Options", padx=10, pady=10)

# 라디오 버튼 상태를 저장할 변수 생성 (인버터 전압, 전류, 주파수 선택용)
radio_var = tk.IntVar()
radio_var.set(0)  # 기본 값 설정

# 인버터 전압, 인버터 전류, 인버터 주파수를 위한 라디오 버튼 생성
radiobutton1 = tk.Radiobutton(checkbox_frame, text="인버터 전압", variable=radio_var, value=1, pady=10, command=lambda: [toggle_rectangle1()])
radiobutton2 = tk.Radiobutton(checkbox_frame, text="인버터 전류", variable=radio_var, value=2, pady=10, command=lambda: [toggle_rectangle2()])
radiobutton3 = tk.Radiobutton(checkbox_frame, text="인버터 주파수", variable=radio_var, value=3, pady=10, command=lambda: [toggle_rectangle3()])

checkbox7 = tk.Checkbutton(checkbox_frame, text="기타", variable=checkbox_var7, pady=20, command=toggle_other_rectangles)



# 사각형의 크기를 업데이트하는 함수
def resize_rectangle(event, rectangle_id):
    canvas_width = event.width
    canvas_height = event.height

    if rectangle_id is not None:
        canvas.delete(rectangle_id)  # 기존 사각형 제거
        # 화면 크기에 비례하여 사각형을 다시 그리기
        return canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="blue")

def raise_other_rectangles():
    for rect_id in other_rectangle_ids:
        canvas.tag_raise(rect_id)  # 기타 사각형을 항상 맨 앞으로 올림
        
# 인버터 전압 라디오 버튼에 따른 사각형 표시/숨김 함수
def toggle_rectangle1():
    global rectangle_id1, rectangle_id2, rectangle_id3
    if radio_var.get() == 1:  # 라디오 버튼이 선택된 경우
        if rectangle_id2 is not None:  # 인버터 전류 사각형이 그려져 있으면 제거
            canvas.delete(rectangle_id2)
            rectangle_id2 = None
        if rectangle_id3 is not None:  # 인버터 주파수 사각형이 그려져 있으면 제거
            canvas.delete(rectangle_id3)
            rectangle_id3 = None
        if rectangle_id1 is None:  # 인버터 전압 사각형이 그려져 있지 않으면 그리기
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            rectangle_id1 = canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="blue")
            canvas.bind("<Configure>", lambda event: resize_rectangle(event, rectangle_id1))  # 창 크기 조정 이벤트에 바인딩
        raise_other_rectangles()  # 기타 사각형을 항상 맨 앞으로 올림
    else:
        if rectangle_id1 is not None:
            canvas.delete(rectangle_id1)
            rectangle_id1 = None

# 인버터 전류 라디오 버튼에 따른 사각형 표시/숨김 함수
def toggle_rectangle2():
    global rectangle_id1, rectangle_id2, rectangle_id3
    if radio_var.get() == 2:  # 라디오 버튼이 선택된 경우
        if rectangle_id1 is not None:  # 인버터 전압 사각형이 그려져 있으면 제거
            canvas.delete(rectangle_id1)
            rectangle_id1 = None
        if rectangle_id3 is not None:  # 인버터 주파수 사각형이 그려져 있으면 제거
            canvas.delete(rectangle_id3)
            rectangle_id3 = None
        if rectangle_id2 is None:  # 인버터 전류 사각형이 그려져 있지 않으면 그리기
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            rectangle_id2 = canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="red")
            canvas.bind("<Configure>", lambda event: resize_rectangle(event, rectangle_id2))  # 창 크기 조정 이벤트에 바인딩
        raise_other_rectangles()  # 기타 사각형을 항상 맨 앞으로 올림
    else:
        if rectangle_id2 is not None:
            canvas.delete(rectangle_id2)
            rectangle_id2 = None

# 인버터 주파수 라디오 버튼에 따른 사각형 표시/숨김 함수
def toggle_rectangle3():
    global rectangle_id1, rectangle_id2, rectangle_id3
    if radio_var.get() == 3:  # 라디오 버튼이 선택된 경우
        if rectangle_id1 is not None:  # 인버터 전압 사각형이 그려져 있으면 제거
            canvas.delete(rectangle_id1)
            rectangle_id1 = None
        if rectangle_id2 is not None:  # 인버터 전류 사각형이 그려져 있으면 제거
            canvas.delete(rectangle_id2)
            rectangle_id2 = None
        if rectangle_id3 is None:  # 인버터 주파수 사각형이 그려져 있지 않으면 그리기
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            rectangle_id3 = canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="yellow")
            canvas.bind("<Configure>", lambda event: resize_rectangle(event, rectangle_id3))  # 창 크기 조정 이벤트에 바인딩
        raise_other_rectangles()  # 기타 사각형을 항상 맨 앞으로 올림
    else:
        if rectangle_id3 is not None:
            canvas.delete(rectangle_id3)
            rectangle_id3 = None


# 메뉴 표시 여부를 저장하는 변수
menu_visible = False

# 메뉴(콤보박스)를 숨기거나 나타내는 함수 정의
def toggle_menu():
    global menu_visible
    if menu_visible:
        checkbox_frame.place_forget()  # 체크박스를 숨김
        toggle_button.config(text="메뉴 나타내기")
    else:
        checkbox_frame.place(x=10, y=50)  # 체크박스를 나타냄
        toggle_button.config(text="메뉴 숨기기")
        # 체크박스 및 라디오 버튼 배치
        radiobutton1.pack(anchor="w")
        radiobutton2.pack(anchor="w")
        radiobutton3.pack(anchor="w")
        checkbox7.pack(anchor="w")
    menu_visible = not menu_visible

# 메뉴 숨기기/나타내기 버튼 생성
toggle_button = tk.Button(window, text="메뉴 숨기기", command=toggle_menu)
toggle_button.place(x=10, y=10)

# 체크박스 프레임 배치
checkbox_frame.place(x=10, y=50)

# 날짜 버튼 생성
date_button = ttk.Button(window, text="날짜")  
date_button.place(x=450,y=0, anchor="n")

notebook = ttk.Notebook(window)
notebook.pack()  # 창 크기에 맞게 확장

# 각 프레임 생성
frame1 = tk.Frame(notebook)
frame2 = tk.Frame(notebook)
frame3 = tk.Frame(notebook)
frame4 = tk.Frame(notebook)

# Notebook에 각 프레임 추가
notebook.add(frame1, text="현황")
notebook.add(frame2, text="발전")
notebook.add(frame4, text="정보")  # '진단' 프레임 앞에 '정보' 프레임 삽입
notebook.add(frame3, text="진단")

# 각 프레임에 내용 추가 (예시)
tk.Label(frame1, text="현황 화면", font=("Arial", 40)).pack(pady=100)
tk.Label(frame2, text="발전 화면", font=("Arial", 40)).pack(pady=100)
tk.Label(frame4, text="정보 화면", font=("Arial", 40)).pack(pady=100)
tk.Label(frame3, text="진단 화면", font=("Arial", 40)).pack(pady=100)

# 메인 루프 실행
window.mainloop()
