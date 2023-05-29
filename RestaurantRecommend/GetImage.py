import urllib.request
import xml.etree.ElementTree as ET
import requests
from PIL import Image
import io

import APIKey

class RestImage:
    def __init__(self, restname):
        self.image = []
        self.cur_num = 0
        client_id = APIKey.naver_api_key
        client_secret = APIKey.naver_Client_Scret
        url = "https://openapi.naver.com/v1/search/image.xml"
        params = {
            "query": restname,
            "display": 6
        }
        headers={
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

        response = requests.get(url, params=params,headers=headers)

        root = ET.fromstring(response.content)
        t = eval(root.findtext(".//total"))
        if t <6: self.total = t
        else : self.total = 6



        items = root.findall(".//item")  # items에 정보들 저장
        a = 0
        for item in items:
            a += 1
            image_url = item.findtext("link")

            self.image.append(image_url)
    def GetCurImage(self):
        return self.image[self.cur_num]