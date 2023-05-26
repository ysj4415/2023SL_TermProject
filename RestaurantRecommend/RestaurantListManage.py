import requests
import xml.etree.ElementTree as ET

import APIKey
import information as inf

size = 500             #한번에 가져오는 데이터의 양
class RLM:
    def __init__(self):
        self.restaurants = {}           # restaurants[지역][메뉴]
        # self.GetData_SIGUN(inf.current_menu,'안양시')
        self.GetData(inf.current_menu)

        # ------ 시,군 리스트 생성 ------
        if not inf.isFullSiGun:
            inf.l_SIGUN = list(self.restaurants.keys())
            inf.isFullSiGun = True


        for a in self.restaurants:
            print(a,end=': ')

            print(self.restaurants[a])

    def GetData_response(self, response):
        root = ET.fromstring(response.content)
        items = root.findall(".//row")  # items에 정보들 저장
        for item in items:
            # ------ 필요한 정보들로 딕셔너리 생성 ------
            restaurant = {
                "name": item.findtext("BIZPLC_NM"),  # 가게 이름
                "address": item.findtext("REFINE_ROADNM_ADDR"),  # 가게 주소
            }
            SIGUN_NM = item.findtext("SIGUN_NM")
            if not SIGUN_NM in self.restaurants:  # 시군명이 없으면 해당 시군명을 키값으로 가지는 밸류에 딕셔너리 추가
                self.restaurants[SIGUN_NM] = {}
            if not inf.current_menu in self.restaurants[SIGUN_NM]:  # 메뉴명이 없으면 해당 메뉴명을 키값으로 가지는 밸류에 리스트 추가
                self.restaurants[SIGUN_NM][inf.current_menu] = []
            self.restaurants[SIGUN_NM][inf.current_menu].append(restaurant)  # 해당 시군명과 메뉴명을 키값으로 가지는 리스트에 가게 정보 추가

    def GetData_SIGUN(self, menu, SIGUN):
        url = "https://openapi.gg.go.kr/" + inf.menu[menu]
        listcount = self.GetListCount(menu, SIGUN)
        for i in range(1,listcount // size+2):
            params = {
                "KEY": APIKey.Data_api_key,
                "pIndex": i,  # 1페이지 요청
                "pSize": size,  # 한 페이지에 500개의 데이터 요청
                "SIGUN_NM": SIGUN
            }
            response = requests.get(url, params=params)
            self.GetData_response(response)

    def GetData(self, menu):
        url = "https://openapi.gg.go.kr/" + inf.menu[menu]
        listcount = self.GetListCount(menu, '')
        for i in range(1,listcount // size+2):
            params = {
                "KEY": APIKey.Data_api_key,
                "pIndex": i,  # 1페이지 요청
                "pSize": size  # 한 페이지에 500개의 데이터 요청
            }
            response = requests.get(url, params=params)
            self.GetData_response(response)

    def GetListCount(self, menu, SIGUN):
        url = "https://openapi.gg.go.kr/" + inf.menu[menu]
        if SIGUN == '':
            params = {
                "KEY": APIKey.Data_api_key,
                "pIndex": 1,  # 1페이지 요청
                "pSize": 1
            }
        else:
            params = {
                "KEY": APIKey.Data_api_key,
                "pIndex": 1,  # 1페이지 요청
                "pSize": 1,
                "SIGUN_NM": SIGUN
            }
        response = requests.get(url, params=params)
        root = ET.fromstring(response.content)
        item = root.find(".//head")
        return eval(item.findtext('list_total_count'))
RLM()
