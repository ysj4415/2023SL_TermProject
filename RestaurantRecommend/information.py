#---------------- 메뉴 명 딕셔너리 ---------------------
menu = {'김밥(도시락)':'Genrestrtlunch', '카페':'Genrestrtcate', '중식':'Genrestrtchifood',
        '일식':'Genrestrtjpnfood','탕':'Genrestrtsoup','회':'Genrestrtsash',
        '패스트푸드':'Genrestrtfastfood','뷔페':'Genrestrtbuff'}
menulist = list(menu.keys())

#---------------- 시군 명, 시군 코드 ---------------------
isFullSiGun = False                 # 시군 리스트가 채워졌는지
l_SIGUN = []                        # 시군명 정보(key)현재


#---------------- tkinter에서 현재 가리키고 있는 시군명, 메뉴명 ---------------------
current_SIGUN = ''
current_menu = menulist[0]