'''
csv 열 설명
1 : 일련번호
2 : 식당이름
3 : 식당지점이름
4 : 식당주소
5 : 식당평점
6 : 리뷰평점
7 : 리뷰본문
8 : 리뷰작성일시
9 ~ 38 : 사진
'''

import pandas as pd
import sys, os
import urllib.request

import tkinter as tk
from tkinter import filedialog

# 윈도우 만들기
root = tk.Tk()
root.title("망고플레이트 백업 프로그램")
root.geometry("500x150+100+100")
root.resizable(False, False)

filename = ''
status = ""

# 파일 불러오기 함수
def openfile():
    global filename
    filename = filedialog.askopenfilename(initialdir="./", title="파일 열기", filetypes=(
        ("CSV", "*.csv"), ("모든 파일", "*.*")
    ))

'''
"백업 시작" 버튼을 클릭하면 전체 행에 대한 반복
1. 폴더 생성
2. 폴더 안에 텍스트 파일 저장
3. 폴더 안에 이미지 파일 저장
'''
def startBackup():
    global filename, status
    
    df = pd.read_csv(filename)
    os.makedirs("나의 망고플레이트 기록", exist_ok=True)

    for row in df.itertuples():
        # 폴더 이름 짓기
        restname = row[2].replace(" ", "_")
        if isinstance(row[3], str):
            branchname = row[3].replace(" ", "_")
        else:
            branchname=""
        rvdate = str(row[8])[:10]

        foldername = restname + branchname + rvdate + str(row[1])

        # 폴더 생성
        new_Folder = "나의 망고플레이트 기록/" + foldername
        os.makedirs(new_Folder, exist_ok=True)

        # 리뷰 텍스트 다운로드
        rvtxt = open(new_Folder + '/' + foldername + '.txt', 'w', encoding="utf-8")
        rvtxt.write(row[7])
        rvtxt.close()

        # 리뷰 이미지 다운로드
        # row 8~37
        img = 1
        for i in range(9, 38):
            if isinstance(row[i], str):
                urllib.request.urlretrieve(row[i], new_Folder + '/' + restname + str((i-8)) + ".jpg")

if __name__ == "__main__":
    # 로드 버튼
    btn_Load = tk.Button(root, text="파일 불러오기", command=openfile, width=14, height = 2)
    btn_Load.grid(row=0, column=0, padx=5, pady = 20)

    # 파일 이름 표시
    label_afterLoad = tk.Label(root, text="파일 이름이 여기에 표시됩니다.", width=50, height=2)
    label_afterLoad.grid(row=0, column=1, padx = 5, pady=20)

    # 백업 버튼
    btn_Backup = tk.Button(root, text = "백업", command=startBackup, width = 15, height = 2)
    btn_Backup.grid(row=2, column=1, pady = 1)

    while True:
        if filename != '':
            break
        root.update()

    label_afterLoad = tk.Label(root, text = filename, width=50, height=2)
    label_afterLoad.grid(row=0, column=0, columnspan=15, padx = 5, pady=20)

    # 메인함수 tkinter 실행
    root.mainloop()