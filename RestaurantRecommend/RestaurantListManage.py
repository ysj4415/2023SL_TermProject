import requests
import xml.etree.ElementTree as ET
from tkinter import *
import tkinter as tk
import tkinter.ttk

import spam
import information as inf

import threading
size = 1000             #한번에 가져오는 데이터의 양


class RLM:
    def __init__(self, window):
        self.restaurants = {}           # restaurants[지역][메뉴]
        # self.rest = [[[] for _ in range(len(inf.menu_num))]for _ in range(len(inf.Gyeonggi))]


        self.pb = tkinter.ttk.Progressbar(window, maximum=100, mode="determinate",length=300)
        self.pb.pack(anchor="center")

        self.label = Label(window, text="데이터 가져오는 중")
        self.label.pack(anchor="center")
        window.update()
        # self.pb['maximum'] = len(inf.menu)
        self.GetData(inf.current_menu)
        self.pb.destroy()
        self.label.destroy()
        # ------------------------------------------- 추가 -------------------------------------------
        # 지역화폐 가맹점, 모범 음식점 현황 데이터

        # ------ 시,군 리스트 생성 ------
        if not inf.isFullSiGun:
            inf.l_SIGUN = list(self.restaurants.keys())
            inf.isFullSiGun = True
        inf.current_SIGUN = inf.l_SIGUN[0]

        # sum = 0
        # for a in self.restaurants:
        #     for b in self.restaurants[a]:
        #         for c in self.restaurants[a][b]:
        #             sum+=1
        #     print(a, ': ', sum)
        #     sum = 0


    def GetData_response(self, num, menu, tele=False):
        url = "https://openapi.gg.go.kr/" + inf.menu[menu]

        params = {
            "KEY": spam.getdataID(),
            "pIndex": num,  # 1페이지 요청
            "pSize": size  # 한 페이지에 500개의 데이터 요청
        }

        response = requests.get(url, params=params)


        root = ET.fromstring(response.content)
        items = root.findall(".//row")  # items에 정보들 저장
        for item in items:
            if item.findtext("BSN_STATE_NM") == '영업':
                # ------ 필요한 정보들로 딕셔너리 생성 ------
                restaurant = {
                    "name": item.findtext("BIZPLC_NM"),  # 가게 이름
                    "address": item.findtext("REFINE_ROADNM_ADDR"),  # 가게 주소
                    "lat": item.findtext("REFINE_WGS84_LAT"),   #위도
                    "log": item.findtext("REFINE_WGS84_LOGT"),   #경도
                    "isParag": False,
                    "isRMny": False
                }

                SIGUN_NM = item.findtext("SIGUN_NM")
                if not SIGUN_NM in self.restaurants:  # 시군명이 없으면 해당 시군명을 키값으로 가지는 밸류에 딕셔너리 추가
                    self.restaurants[SIGUN_NM] = {}
                if not menu in self.restaurants[SIGUN_NM]:  # 메뉴명이 없으면 해당 메뉴명을 키값으로 가지는 밸류에 리스트 추가
                    self.restaurants[SIGUN_NM][menu] = []
                self.restaurants[SIGUN_NM][menu].append(restaurant)  # 해당 시군명과 메뉴명을 키값으로 가지는 리스트에 가게 정보 추가
                # self.rest[SIGUN_NM][menu].append(restaurant)
            if tele == False:
                self.pb.step(1)
                self.pb.update()

    def GetData(self, menu, tele=False):

        listcount = self.GetListCount(inf.menu[menu], '')
        #----------초기화-------------
        # self.pb.update()
        if tele == False:
            self.pb['maximum']=listcount
        #----------초기화-------------
        for i in range(1,listcount // size+2):

            self.GetData_response(i, menu, tele)



    def GetListCount(self, address, SIGUN):
        url = "https://openapi.gg.go.kr/" + address
        if SIGUN == '':
            params = {
                "KEY": spam.getdataID(),
                "pIndex": 1,  # 1페이지 요청
                "pSize": 1
            }
        else:
            params = {
                "KEY": spam.getdataID(),
                "pIndex": 1,  # 1페이지 요청
                "pSize": 1,
                "SIGUN_NM": SIGUN
            }
        response = requests.get(url, params=params)
        root = ET.fromstring(response.content)
        item = root.find(".//head")

        if item:
            # print(eval(item.findtext('list_total_count')))
            return eval(item.findtext('list_total_count'))
        else: return 0

    def GetRestList_Update(self, menu, SIGUN, window):
        # if self.rest[inf.Gyeonggi[SIGUN]][inf.menu_num[menu]] == []:
        if not menu in self.restaurants[SIGUN]:
            self.pb = tkinter.ttk.Progressbar(window, maximum=100, mode="determinate", length=300)
            self.pb.pack(anchor="center")

            self.label = Label(window, text="데이터 가져오는 중")
            self.label.pack(anchor="center")

            self.GetData(menu)

            self.pb.destroy()
            self.label.destroy()
        restlist = self.restaurants[SIGUN][menu]

        return restlist
    def GetRestList(self, menu, SIGUN, tele=False):
        if tele == False:
            if menu in self.restaurants[SIGUN]:
                restlist = self.restaurants[SIGUN][menu]
                return restlist
            else:
                return []
        else:
            result = []
            if menu in self.restaurants[SIGUN]:
                restlist = self.restaurants[SIGUN][menu]
                for r in restlist:
                    result.append(r['name'] + ': ' + r['address'])
                return result
            else:
                self.GetData(menu, tele= True)
                restlist = self.restaurants[SIGUN][menu]
                for r in restlist:
                    result.append(r['name'] + ': ' + r['address'])
                return result

    def GetParagonRestList(self, menu, SIGUN):
        listcount = self.GetListCount('ParagonRestaurant', SIGUN)
        # ----------초기화-------------
        # self.pb.update()
        # ----------초기화-------------
        for i in range(1, listcount // size + 2):

            url = "https://openapi.gg.go.kr/" + inf.menu[menu]

            params = {
                "KEY": spam.getdataID(),
                "pIndex": i,  # 1페이지 요청
                "pSize": size,  # 한 페이지에 500개의 데이터 요청
                "SIGUN_NM": SIGUN
            }

            response = requests.get(url, params=params)

            root = ET.fromstring(response.content)
            items = root.findall(".//row")  # items에 정보들 저장
            for item in items:
                if item.findtext("BSN_STATE_NM") == '영업':
                    # ------ 필요한 정보들로 딕셔너리 생성 ------
                    restaurant = {
                        "name": item.findtext("BIZPLC_NM"),  # 가게 이름
                        "address": item.findtext("REFINE_ROADNM_ADDR"),  # 가게 주소
                        "lat": item.findtext("REFINE_WGS84_LAT"),  # 위도
                        "log": item.findtext("REFINE_WGS84_LOGT"),  # 경도
                        "isParag": False,
                        "isRMny": False
                    }

                    SIGUN_NM = item.findtext("SIGUN_NM")
                    if not SIGUN_NM in self.restaurants:  # 시군명이 없으면 해당 시군명을 키값으로 가지는 밸류에 딕셔너리 추가
                        self.restaurants[SIGUN_NM] = {}
                    if not menu in self.restaurants[SIGUN_NM]:  # 메뉴명이 없으면 해당 메뉴명을 키값으로 가지는 밸류에 리스트 추가
                        self.restaurants[SIGUN_NM][menu] = []
                    self.restaurants[SIGUN_NM][menu].append(restaurant)  # 해당 시군명과 메뉴명을 키값으로 가지는 리스트에 가게 정보 추가
                    # self.rest[SIGUN_NM][menu].append(restaurant)
