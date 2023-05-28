from tkinter import *
import tkinter as tk
import tkinter.ttk
from googlemaps import Client
import requests
import io
from PIL import Image, ImageTk
import APIKey
from RestaurantListManage import RLM
import information as inf

zoom = 10
w_width = 1000
w_height = 600

bs = 10         #하단 프레임 사이 간격

class MainGUI:
    def CB_CheckChange(self):
        if self.cb_regionselect.get() == inf.current_SIGUN and self.cb_menulist.get() == inf.current_menu:
            return True
        else: return False
    def CB_ChangeCurrent(self):
        inf.current_menu = self.cb_menulist.get()
        inf.current_SIGUN = self.cb_regionselect.get()
        self.list = self.restlist.GetRestList(inf.current_menu, inf.current_SIGUN)

        self.ListBoxUpdate()
    def ListBoxUpdate(self):                # 리스트 박스의 항목 업데이트
        s = self.listbox.size()
        self.listbox.delete(0,s-1)
        for line in range(len(self.list)):
            self.listbox.insert(line, self.list[line]['name'])
    def __init__(self):
        self.window = Tk()
        self.window.title('경기도 맛집 추천')
        self.window.geometry(str(w_width) + 'x' + str(w_height))
        self.window.resizable(False, False)         # 윈도우 창 크기 조절 불가
        # self.canvas = Canvas(self.window,bg = 'white', width=400, height=300)
        # self.canvas.pack()

        self.restlist = RLM()                #식당리스트
        self.list = self.restlist.GetRestList(inf.current_menu, inf.current_SIGUN)
        '''------------------------------------ 상단 프레임 ---------------------------------'''
        frame1 = tkinter.Frame(self.window, relief='solid', bd=2)
        f1_width, f1_height = w_width - 100, 100
        frame1.place(x=50, y=0, width=f1_width, height=f1_height)

        # 지역 선택 리스트
        values = [str(i) + "번" for i in range(1,101)]
        self.cb_regionselect = tkinter.ttk.Combobox(frame1,height=15, values=inf.l_SIGUN,exportselection=False,
                                                    validate='focus',validatecommand=self.CB_CheckChange,invalidcommand=self.CB_ChangeCurrent)
        self.cb_regionselect.place(x=0, y=30, width=200, height=40)

        self.cb_regionselect.current(0)

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

        self.cb_menulist = tkinter.ttk.Combobox(frame2,height=4, values=inf.menulist,exportselection=False,
                                                validate='focus',validatecommand=self.CB_CheckChange,invalidcommand=self.CB_ChangeCurrent)
        self.cb_menulist.pack(side='top', fill='x')
        self.cb_menulist.current(0)

        self.b_openstate = Button(frame2,text='정보 열기')
        self.b_openstate.pack(side='bottom',fill='x')

        self.scrollbar = tkinter.Scrollbar(frame2)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tkinter.Listbox(frame2, yscrollcommand=self.scrollbar.set)
        for line in range(len(self.list)):
            self.listbox.insert(line, self.list[line]['name'])
        self.listbox.pack(side="left", fill='both',expand=True)

        self.scrollbar["command"] = self.listbox.yview

        self.b_rest1 = Button(frame2, text='')


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
        Google_API_Key = APIKey.google_api_key
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