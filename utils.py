import os
import  datetime 
import time
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_template_message(reply_token, template):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, template)

    return "OK"

def active_send_text_msg(uid,msg,timer,number):
    print("start to wait for "+str(timer))
    waitRate=(number['target']-number['now'])
    line_bot_api = LineBotApi(channel_access_token)
    time.sleep(timer.seconds*waitRate)
    line_bot_api.push_message(uid, TextSendMessage(text=msg))

def active_send_clock_msg(uid,msg,timer,number,index,fun,get_name):
    print("start to wait for "+str(timer))
    waitRate=(number['target']-number['now'])
    start=datetime.datetime.now()
    setTime=datetime.timedelta(hours=start.hour,minutes = start.minute, seconds = start.second)
    line_bot_api = LineBotApi(channel_access_token)
    time.sleep(timer.seconds*waitRate)
    name=get_name(index)
    if(name!=None):
        line_bot_api.push_message(uid, TextSendMessage(text=name+msg+" ("+str(setTime)+"設定的號碼牌)"))
    else:
        line_bot_api.push_message(uid, TextSendMessage(text=msg+" ("+str(setTime)+"設定的號碼牌)"))
    fun(index)

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
