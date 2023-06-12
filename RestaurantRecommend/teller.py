import telepot
import noti
import spam
import information
import os
import json

def replyResData(rlm, user, menu=information.current_menu,SIGUN=information.current_SIGUN ):
    noti.sendMessage(user, '데이터 불러오는 중')
    msg = ''
    list = rlm.GetRestList(menu, SIGUN, tele=True)
    for r in list:
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '데이터가 없습니다.')

def replymemoData(user, name):
    file = "save.json"
    if os.path.isfile(file):
        count = 0
        with open(file) as f:
            d = json.load(f)
        if d == None: return 0

        for sigun in information.l_SIGUN:
            if name+sigun in d:
                msg = name + '\n별점: ' + str(d[name+sigun]['score']) + '\n메모: \n' + d[name+sigun]['memo']
                count += 1

                noti.sendMessage( user, msg )
        if count == 0:
            msg = '해당 가게에 작성하신 메모가 없습니다.'
            noti.sendMessage(user, msg)

def handle(msg, rlm):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')
    if text.startswith('음식점') and len(args) == 1:
        replyResData(rlm , chat_id)
    elif text.startswith('음식점') and len(args) > 1:
        replyResData(rlm , chat_id, args[1], args[2])
    elif text.startswith('메모확인') and len(args) > 1:
        s = ''
        for i in range(len(args) - 1):
            s = s + args[i+1]
            if i < len(args) - 2:
                s += ' '
        replymemoData(chat_id, s)
    # elif text.startswith('확인'):
    #     print('try to 확인')
    #     check( chat_id )
    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n음식점,  음식점 [종류] [지역],  메모확인 [음식점 이름] 중 하나의 명령을 입력하세요.')




bot = telepot.Bot(spam.gettokenID())
