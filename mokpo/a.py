import tkinter as tk
import pandas as pd

def load_csv_to_canvas(canvas, file_path="mokpo/info1.csv"):
    # CSV 파일을 Pandas DataFrame으로 읽기
    df = pd.read_csv(file_path)
    
    # 초기 좌표 설정
    x, y = 10, 10  # 시작 좌표 (10, 10)
    y_offset = 20  # 각 행 간의 간격
    x_offset = 100  # 열 간의 간격
    
    # Canvas 크기 조정 (DataFrame의 크기에 맞춰)
    canvas_width = max(500, x_offset * len(df.columns))  # 열의 수에 맞춰 가로 크기
    canvas_height = y + (y_offset * len(df))  # 데이터 행의 수에 맞춰 세로 크기
    canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
    
    # DataFrame의 열 이름 표시
    headers = " | ".join(df.columns)
    canvas.create_text(x, y, anchor="nw", text=headers, fill="blue")
    y += y_offset
    
    # DataFrame의 각 행을 Canvas에 추가
    for index, row in df.iterrows():
        row_text = " | ".join(map(str, row.values))
        canvas.create_text(x, y, anchor="nw", text=row_text, fill="black")
        y += y_offset

# Tkinter 윈도우 및 Canvas 설정
root = tk.Tk()
root.title("CSV Data Viewer")

# 스크롤을 위한 캔버스와 스크롤바 추가
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# CSV 파일을 Canvas에 로드
load_csv_to_canvas(canvas, "info1.csv")

root.mainloop()
