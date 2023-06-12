import sys
import telepot
import traceback
import spam

MAX_MSG_LENGTH = 300
bot = telepot.Bot(spam.gettokenID())


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

