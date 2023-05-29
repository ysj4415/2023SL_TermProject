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
import GetImage

zoom = 11
w_width = 1000
w_height = 600

bs = 10         #하단 프레임 사이 간격
marker_max_count = 100


class MainGUI:
    def CB_CheckChange(self):
        if self.cb_regionselect.get() == inf.current_SIGUN and self.cb_menulist.get() == inf.current_menu:
            return True
        else: return False
    def CB_ChangeCurrent(self):
        inf.current_menu = self.cb_menulist.get()
        inf.current_SIGUN = self.cb_regionselect.get()
        self.listbox.destroy()
        self.b_openstate['state'] = 'disabled'
        self.b_random['state'] = 'disabled'
        self.b_search['state'] = 'disabled'
        self.list = self.restlist.GetRestList_Update(inf.current_menu, inf.current_SIGUN, self.frame2)
        self.b_openstate['state'] = 'active'
        self.b_random['state'] = 'active'
        self.b_search['state'] = 'active'
        self.ListBoxUpdate()
        self.UpdateMap()
        self.UpdateGraph()

        self.search()
    def ListBoxUpdate(self):                # 리스트 박스의 항목 업데이트
        self.listbox = tkinter.Listbox(self.frame2, yscrollcommand=self.scrollbar.set)
        for line in range(len(self.list)):
            self.listbox.insert(line, self.list[line]['name'])
        self.listbox.pack(side="left", fill='both',expand=True)

        self.listbox.bind("<ButtonRelease-1>",self.ClickListBox)

        self.scrollbar["command"] = self.listbox.yview
        self.select_index = 0
        self.label['text']=str(self.select_index) + "/" + str(len(self.list))


    def ClickListBox(self,event):
        self.select_index = self.listbox.curselection()[0] + 1
        self.label['text']=str(self.select_index) + "/" + str(len(self.list))
    def leftbuttonimage(self):

        self.rest_image.cur_num -= 1
        self.label4['text'] = str(self.rest_image.cur_num + 1) + '/' + str(self.rest_image.total)

        if self.rightButton['state'] == 'disabled': self.rightButton['state'] ='active'
        res = requests.get(self.rest_image.GetCurImage())

        im = Image.open(io.BytesIO(res.content))
        im_resize = im.resize((400, 300))
        self.p = ImageTk.PhotoImage(im_resize)
        self.label3['image'] = self.p

        if self.rest_image.cur_num == 0: self.leftButton['state'] = 'disabled'
    def rightbuttonimage(self):
        self.rest_image.cur_num += 1
        self.label4['text'] = str(self.rest_image.cur_num + 1) + '/' + str(self.rest_image.total)

        if self.leftButton['state'] == 'disabled': self.leftButton['state'] = 'active'
        res = requests.get(self.rest_image.GetCurImage())

        im = Image.open(io.BytesIO(res.content))
        im_resize = im.resize((400, 300))
        self.p = ImageTk.PhotoImage(im_resize)
        self.label3['image'] = self.p

        if self.rest_image.cur_num == self.rest_image.total-1: self.rightButton['state'] = 'disabled'
    def OpenState(self):
        if self.select_index == 0:
            return 0

        current_index = self.select_index - 1
        '''------------------------------------ 외부 윈도우 ---------------------------------'''
        if self.toplevel != None: self.toplevel.destroy()
        self.toplevel=tkinter.Toplevel(self.window)
        self.toplevel.geometry("600x400+820+100")
        self.toplevel.title(self.list[current_index]['name'])

        self.notebook = tkinter.ttk.Notebook(self.toplevel, width=300, height=300)
        self.notebook.pack(fill='both',expand=True)

        frame1 = tkinter.Frame(self.toplevel)
        self.notebook.add(frame1, text="정보")

        label1 = tkinter.Label(frame1, text=self.list[current_index]['name'])
        label1.pack()
        label2 = tkinter.Label(frame1, text=self.list[current_index]['address'])
        label2.pack()

        self.leftButton = Button(frame1,overrelief="solid", text='<',command=self.leftbuttonimage,state='disabled')
        self.leftButton.pack(side='left')

        self.rightButton = Button(frame1,overrelief="solid", text='>',command=self.rightbuttonimage)
        self.rightButton.pack(side='right')



        self.rest_image=GetImage.RestImage(self.list[current_index]['name'])
        if self.rest_image.total == 1: self.rightButton['state'] = 'disable'
        if self.rest_image.total == 0:
            self.label3=tkinter.Label(frame1, text='해당 이미지가 없습니다.')
            self.label3.pack()
            self.rightButton['state']='disabled'
        else:
            res = requests.get(self.rest_image.GetCurImage())

            im = Image.open(io.BytesIO(res.content))
            im_resize = im.resize((400,300))
            self.p = ImageTk.PhotoImage(im_resize)
            self.label3 = tkinter.Label(frame1, image=self.p)
            # label3['image']=photo
            self.label3.pack()

        self.label4 = Label(frame1,text=str(self.rest_image.cur_num + 1) + '/' + str(self.rest_image.total))
        self.label4.pack(side='bottom', anchor='center')

        '''------------------------------------ 메모 기능 ---------------------------------'''

        frame2 = tkinter.Frame(self.toplevel)
        self.notebook.add(frame2, text="노트")

        frame2_1 = tkinter.Frame(frame2)
        frame2_1.pack(side='top',fill='x')

        frame2_2 = tkinter.Frame(frame2)
        frame2_2.pack(side='bottom',fill='both')

        self.f2_label = Label(frame2_1,text='별점: ')
        self.f2_label.grid(row=0, column=0)

        self.Text = Text(frame2_2)
        self.Read()
        self.Text.pack(fill='both',expand=True)
        self.enterbutton = Button(frame2_2, text='저장', command=self.Save)
        self.enterbutton.pack(side='bottom')
    def Save(self):
        f = open("save", 'a')
        current_index = self.select_index - 1
        f.write(self.list[current_index]['name']+'\n')
        f.write(self.Text.get(1.0,10.100))
        f.write('                  \n')

        f.close()
    def Read(self):
        f = open("save", 'r')
        current_index = self.select_index - 1

        while True:
            line = f.readline()
            if line == self.list[current_index]['name'] + '\n':
                i = 1.0
                while(True):
                    if line != '                  \n':
                        line = f.readline()
                        self.Text.insert(i,line)
                        i+=1.0
                    else: break
                break
            if not line: break
        f.close()

    def UpdateMap(self):
        # 지도 생성
        gmaps = Client(key=APIKey.google_api_key)
        center = gmaps.geocode(inf.current_SIGUN)[0]['geometry']['location']
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={center['lat']},{center['lng']}&zoom={zoom}&size=400x400&maptype=roadmap"

        #마커 추가
        mark_num = 0
        for rest in self.list:
            if rest['lat'] and rest['log']:
                lat, log = float(rest['lat']), float(rest['log'])
                marker_url = f"&markers=color:red%7C{lat},{log}"
                map_url += marker_url
            mark_num += 1
            if mark_num >= marker_max_count:
                break

        # 서울시 지도 이미지 다운로드
        response = requests.get(map_url + '&key=' + APIKey.google_api_key)
        image = Image.open(io.BytesIO(response.content))
        self.photo = ImageTk.PhotoImage(image)
        self.map_label['image'] = self.photo

    def UpdateGraph(self):
        self.canvas.delete('all')

        max_count = 0
        for SIGUN in inf.l_SIGUN:
            a = len(self.restlist.GetRestList(inf.current_menu, SIGUN))
            if max_count < a:
                max_count = a


        bar_width = 25
        x_gap = 25
        x0 = 10
        y0 = 240

        for i in range(len(inf.l_SIGUN)):
            if self.e_search.get() == '':
                count = len(self.restlist.GetRestList(inf.current_menu, inf.l_SIGUN[i]))
            else:
                text = self.e_search.get()
                l = self.restlist.GetRestList(inf.current_menu, inf.l_SIGUN[i])
                count = 0
                for r in l:
                    if r['name'].find(text) != - 1 or r['address'].find(text) != -1:
                        count +=1
            x1 = x0 + i * (bar_width + x_gap)
            y1 = y0 - 200 * count / max_count
            self.canvas.create_rectangle(x1, y1, x1 + bar_width, y0, fill='blue')
            self.canvas.create_text(x1 + bar_width / 2, y0, text=inf.l_SIGUN[i], anchor='n')
            self.canvas.create_text(x1 + bar_width / 2, y1 - 10, text=str(count), anchor='s')
        self.canvas['scrollregion']=(0,0, x0 + (len(inf.l_SIGUN) - 1) * (bar_width + x_gap) + 50, 500)
    def search(self):
        findword = self.e_search.get()
        newlist=[]
        originlist = self.restlist.GetRestList(inf.current_menu,inf.current_SIGUN)

        for res in originlist:
            if res['name'].find(findword) != -1 or res['address'].find(findword) != -1:
                newlist.append(res)
        self.list = newlist
        self.listbox.destroy()
        self.ListBoxUpdate()
        self.UpdateMap()
        self.UpdateGraph()
    def search_event(self,event):
        self.search()
    def __init__(self):
        f = open("save", 'a')
        f.close()

        self.toplevel = None
        self.window = Tk()
        self.window.title('경기도 맛집 추천')
        self.window.geometry(str(w_width) + 'x' + str(w_height))
        self.window.resizable(False, False)         # 윈도우 창 크기 조절 불가
        # self.canvas = Canvas(self.window,bg = 'white', width=400, height=300)
        # self.canvas.pack()

        self.restlist = RLM(self.window)                #식당리스트
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
        self.e_search = Entry(frame1, justify=LEFT)
        self.e_search.place(x=(f1_width - 300) / 2, y=30, width=300, height=20)
        self.e_search.bind('<Return>', self.search_event)

        self.b_search = Button(frame1, text='검색', command=self.search)
        self.b_search.place(x=(f1_width - 300) / 2 + 300, y=30, width=40, height=20)

        # 랜덤 메뉴 추천
        self.b_random = Button(frame1, text='메뉴 추천')
        self.b_random.place(x=f1_width - 200, y=30, width=150, height=40)

        '''------------------------------------ 하단 음식점 리스트 프레임 ---------------------------------'''
        self.frame2 = tkinter.Frame(self.window, relief='solid', bd=2)
        f2_width = (w_width-bs*4)/3
        f2_height=f2_width + 40
        self.frame2.place(x=10, y=w_height - bs - f2_height, width=f2_width, height=f2_height)

        self.cb_menulist = tkinter.ttk.Combobox(self.frame2,height=4, values=inf.menulist,exportselection=False,
                                                validate='focus',validatecommand=self.CB_CheckChange,invalidcommand=self.CB_ChangeCurrent)
        self.cb_menulist.pack(side='top', fill='x')
        self.cb_menulist.current(0)

        self.select_index = 0

        self.label = tkinter.Label(self.frame2, text=str(self.select_index)+"/"+str(len(self.list)),relief="solid")
        self.label.pack(sid='bottom',anchor='center')

        self.b_openstate = Button(self.frame2,text='정보 열기', command=self.OpenState)       #추가
        self.b_openstate.pack(side='bottom',fill='x')

        self.scrollbar = tkinter.Scrollbar(self.frame2)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tkinter.Listbox(self.frame2, yscrollcommand=self.scrollbar.set)
        for line in range(len(self.list)):
            self.listbox.insert(line, self.list[line]['name'])
        self.listbox.pack(side="left", fill='both',expand=True)

        self.listbox.bind("<ButtonRelease-1>",self.ClickListBox)



        self.scrollbar["command"] = self.listbox.yview



        '''------------------------------------ 하단 그래프 리스트 프레임 ---------------------------------'''
        frame3 = tkinter.Frame(self.window, relief='solid', bd=2)
        f3_width = (w_width-bs*4)/3
        f3_height=f3_width - 40
        frame3.place(x=f2_width+bs*2, y=w_height - bs - f3_height, width=f3_width, height=f3_height)

        self.scrollbar_graph = tkinter.Scrollbar(frame3, orient='horizontal')
        self.scrollbar_graph.pack(side="bottom", fill="x")

        self.canvas = Canvas(frame3, bg = 'white',xscrollcommand=self.scrollbar_graph.set)
        self.canvas.pack(side='top', fill='both')
        self.scrollbar_graph.config(command=self.canvas.xview)

        self.UpdateGraph()

        '''------------------------------------ 하단 지도 프레임 ---------------------------------'''
        frame4 = tkinter.Frame(self.window, relief='solid', bd=2)
        f4_width = (w_width-40)/3
        frame4.place(x=w_width - bs - f4_width, y=w_height - bs - f4_width, width=f4_width, height=f4_width)

        self.photo=None
        self.map_label = tk.Label(frame4,image=self.photo)
        self.map_label.pack(fill='both', expand=True)
        self.UpdateMap()



        self.window.mainloop()


MainGUI()