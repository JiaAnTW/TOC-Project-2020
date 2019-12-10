import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import threading
import time
import datetime
from fsm import TocMachine
from utils import send_text_message

load_dotenv()

userOnline=[]

def clean_offline_user():
    while(True):
        time.sleep(3600*2)
        for user in userOnline:
            clock=datetime.datetime.now()
            now=datetime.timedelta(days=clock.day,hours=clock.hour,minutes=clock.minute,seconds=clock.second)
            if(now-user['lastUpdate']>datetime.timedelta(hours=2)):
                del user['state']
                userOnline.remove(user)

cleaner=threading.Thread(target =  clean_offline_user)
#cleaner.start()    

def check_go_back(state,event):
    goBackStates=["setClock","setTime","setNow","setTarget","clockCenter","setName","setSpotName","setLocationInfo"]
    for goBackState in goBackStates:
        if state == goBackState:
            if state== "clockCenter" and event.message.text!="結束計時":
                return False
            if state == "setClock" and event.message.text != "確定送出":
                return False
            return True
    return False


states = ["init", "center","book", "setClock","clockCenter","setTime","setNumber","setNow","setTarget","setName","locationCenter","setSpotName","setLocationInfo","getLocation"]
transitions=[
        { "trigger": "advance","source": "init","dest": "center","conditions": "is_going_to_center"},
        { "trigger": "advance","source": "center","dest": "setClock","conditions": "is_going_to_setClock"},
        { "trigger": "go_back", "source": "setClock", "dest": "center","conditions": "is_back_to_center"},
        { "trigger": "go_back", "source": "setClock", "dest": "book","conditions": "is_back_to_book"},
        { "trigger": "advance","source": "center","dest": "book","conditions": "is_going_to_book"},
        { "trigger": "go_back", "source": "book", "dest": "center"},
        { "trigger": "advance","source": "book","dest": "setName","conditions": "is_going_to_setName"},
        { "trigger": "advance","source": "book","dest": "setClock","conditions": "is_going_to_setClock"},
        { "trigger": "go_back", "source": "setName", "dest": "book"},
        { "trigger": "advance","source": "book","dest": "locationCenter","conditions": "is_going_to_locationCenter"},
        { "trigger": "go_back", "source": "locationCenter", "dest": "book"},
        { "trigger": "advance","source": "locationCenter","dest": "setSpotName","conditions": "is_going_to_setSpotName"},
        { "trigger": "go_back", "source": "setSpotName", "dest": "locationCenter"},
        { "trigger": "advance","source": "locationCenter","dest": "setLocationInfo","conditions": "is_going_to_setLocationInfo"},
        { "trigger": "go_back", "source": "setLocationInfo", "dest": "locationCenter"},
        { "trigger": "advance","source": "setClock","dest": "clockCenter","conditions": "is_going_to_clockCenter"},
        { "trigger": "cycle","source": "clockCenter","dest": "clockCenter","conditions": "cycle_in_clockCenter"},
        { "trigger": "go_back", "source": "clockCenter", "dest": "setClock"},
        { "trigger": "advance","source": "clockCenter","dest": "setTime","conditions": "is_going_to_setTime"},
        { "trigger": "go_back", "source": "clockCenter", "dest": "setClock"},
        { "trigger": "go_back", "source": "setTime", "dest": "clockCenter"},
        { "trigger": "advance","source": "setClock","dest": "setNumber","conditions": "is_going_to_setNumber"},
        { "trigger": "go_back", "source": "setNumber", "dest": "setClock"},
        { "trigger": "advance","source": "setNumber","dest": "setNow","conditions": "is_going_to_setNow"},
        { "trigger": "go_back", "source": "setNow", "dest": "setNumber"},
        { "trigger": "advance","source": "setNumber","dest": "setTarget","conditions": "is_going_to_setTarget"},
        { "trigger": "go_back", "source": "setTarget", "dest": "setNumber"},
        { "trigger": "error", "source": states, "dest": "init"},
    ]
machine = TocMachine(
    states=states,
    transitions=transitions,
    initial="init",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


def check_user_exsist(uid):
    for i in range(len(userOnline)):
        if(userOnline[i]["uid"]==uid):
            return i
    tmp_machine=TocMachine(states=states,transitions=transitions,initial="init",auto_transitions=False,show_conditions=True)
    userOnline.append({"uid":uid,"state":tmp_machine})
    return len(userOnline)-1

def update_time(index):
    clock=datetime.datetime.now()
    now=datetime.timedelta(days=clock.day,hours=clock.hour,minutes=clock.minute,seconds=clock.second)
    userOnline[index]['lastUpdate']=now


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi("0SLteZR2B5lHmN8jtZrYRLz5kIS9e7YxbG5iJFOsOWTEamfytuROe0T1X5NsjBIf6qjQFVnY4qQjDeKn7ibOSE/U72DQaMyaXE+6FTWGvySNI9JEsJqK3S/xWBi9b46WS7qEIplNTX1SMENaYAT0EgdB04t89/1O/w1cDnyilFU=")
parser = WebhookParser("34bd103fc030554fd8abb36dac789e33")


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"



@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")
    
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    beforeEvent=None
    # if event is MessageEvent and message is TextMessage, then echo text
    i=0
    for event in events:
        index=check_user_exsist(event.source.user_id)
        update_time(index)
        if(event.type=="postback" and userOnline[index]["state"].beforeState=="book"):
            userOnline[index]["state"].set_setName_flag(event.postback.data)
            #response = machine.advance(beforeEvent)
            beforeEvent= None
            continue
        if not isinstance(event, MessageEvent):
            continue
        if event.message.type=="location":
            response = userOnline[index]["state"].go_back(event)
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {userOnline[index]['state'].state}")
        print(f"REQUEST BODY: \n{body}")
        print(f"Before state is {userOnline[index]['state'].beforeState}")
        if (event.message.type=="text" and event.message.text=="返回")or check_go_back(userOnline[index]["state"].state, event):
            response = userOnline[index]["state"].go_back(event)
        elif userOnline[index]["state"].state=="book" and (event.message.text=="更改計時器名稱" or event.message.text=="修改號碼牌內容"):
            #if events[i-1].type=="postback":
                #machine.set_setName_flag(events[i-1].postback.data)
            #else:
                #machine.set_setName_flag(events[i+1].postback.data)
            response = userOnline[index]["state"].advance(event)

        elif userOnline[index]["state"].state=="clockCenter" and (event.message.text=="開始計時"):
            response = userOnline[index]["state"].cycle(event)
        else:
            response = userOnline[index]["state"].advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")
        userOnline[index]["state"].beforeState=userOnline[index]["state"].state
        i=i+1
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    #port = os.environ.get("PORT", 8000)
    port = os.environ['PORT']
    app.run(host="0.0.0.0", port=port, debug=True)

