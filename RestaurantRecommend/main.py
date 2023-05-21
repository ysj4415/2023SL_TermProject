from tkinter import *
import tkinter as tk
import tkinter.ttk
from googlemaps import Client
import requests
import io
from PIL import Image, ImageTk

zoom = 10
w_width = 1000
w_height = 600

bs = 10         #하단 프레임 사이 간격

class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('경기도 맛집 추천')
        self.window.geometry(str(w_width) + 'x' + str(w_height))
        self.window.resizable(False, False)         # 윈도우 창 크기 조절 불가
        # self.canvas = Canvas(self.window,bg = 'white', width=400, height=300)
        # self.canvas.pack()

        '''------------------------------------ 상단 프레임 ---------------------------------'''
        frame1 = tkinter.Frame(self.window, relief='solid', bd=2)
        f1_width, f1_height = w_width - 100, 100
        frame1.place(x=50, y=0, width=f1_width, height=f1_height)

        # 지역 선택 리스트
        values = [str(i) + "번" for i in range(1,101)]
        self.cb_regionselect = tkinter.ttk.Combobox(frame1,height=15, values=values)
        self.cb_regionselect.place(x=0, y=30, width=200, height=40)

        # 가게 이름 검색
        self.e_search = Entry(frame1, justify=RIGHT)
        self.e_search.place(x=(f1_width - 300) / 2, y=30, width=300, height=20)

        self.b_search = Button(frame1, text='검색')
        self.b_search.place(x=(f1_width - 300) / 2 + 300, y=30, width=40, height=20)

        # 랜덤 메뉴 추천
        self.b_random = Button(frame1, text='메뉴 추천')
        self.b_random.place(x=f1_width - 200, y=30, width=150, height=40)

        '''------------------------------------ 하단 음식점 리스트 프레임 ---------------------------------'''
        frame2 = tkinter.Frame(self.window, relief='solid', bd=2)
        f2_width = (w_width-bs*4)/3
        f2_height=f2_width + 40
        frame2.place(x=10, y=w_height - bs - f2_height, width=f2_width, height=f2_height)

        '''------------------------------------ 하단 그래프 리스트 프레임 ---------------------------------'''
        frame3 = tkinter.Frame(self.window, relief='solid', bd=2)
        f3_width = (w_width-bs*4)/3
        f3_height=f3_width - 40
        frame3.place(x=f2_width+bs*2, y=w_height - bs - f3_height, width=f3_width, height=f3_height)

        '''------------------------------------ 하단 지도 프레임 ---------------------------------'''
        frame4 = tkinter.Frame(self.window, relief='solid', bd=2)
        f4_width = (w_width-40)/3
        frame4.place(x=w_width - bs - f4_width, y=w_height - bs - f4_width, width=f4_width, height=f4_width)

        # 지도 생성
        Google_API_Key = 'AIzaSyBRC5NtAIU2gf5Gic6DSf-Q1Ye8c7g3jVU'
        gmaps = Client(key=Google_API_Key)
        seoul_center = gmaps.geocode("정왕역")[0]['geometry']['location']
        seoul_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={seoul_center['lat']},{seoul_center['lng']}&zoom={zoom}&size=400x400&maptype=roadmap"

        # 서울시 지도 이미지 다운로드
        response = requests.get(seoul_map_url + '&key=' + Google_API_Key)
        image = Image.open(io.BytesIO(response.content))
        photo = ImageTk.PhotoImage(image)
        map_label = tk.Label(frame4, image=photo)
        map_label.pack(fill='both', expand=True)


        self.window.mainloop()


MainGUI()