import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

def check_go_back(state,event):
    goBackStates=["setClock","setTime","setNow","setTarget","clockCenter","setName"]
    for goBackState in goBackStates:
        if state == goBackState:
            if state== "clockCenter" and event.message.text!="結束計時":
                return False
            if state == "setClock" and event.message.text != "確定送出":
                return False
            return True
    return False

machine = TocMachine(
    states=["init", "center","book", "setClock","clockCenter","setTime","setNumber","setNow","setTarget","setName"],
    transitions=[
        { "trigger": "advance","source": "init","dest": "center","conditions": "is_going_to_center"},
        
        { "trigger": "advance","source": "center","dest": "setClock","conditions": "is_going_to_setClock"},
        { "trigger": "go_back", "source": "setClock", "dest": "center"},

        { "trigger": "advance","source": "center","dest": "book","conditions": "is_going_to_book"},
        { "trigger": "go_back", "source": "book", "dest": "center"},

        { "trigger": "advance","source": "book","dest": "setName","conditions": "is_going_to_setName"},
        { "trigger": "go_back", "source": "setName", "dest": "book"},

        { "trigger": "advance","source": "setClock","dest": "clockCenter","conditions": "is_going_to_clockCenter"},
        { "trigger": "cycle","source": "clockCenter","dest": "clockCenter","conditions": "cycle_in_clockCenter"},
        { "trigger": "go_back", "source": "clockCenter", "dest": "setClock"},

        { "trigger": "advance","source": "clockCenter","dest": "setTime","conditions": "is_going_to_setTime"},
        { "trigger": "go_back", "source": "clockCenter", "dest": "setClock"},

        { "trigger": "advance","source": "setClock","dest": "setNumber","conditions": "is_going_to_setNumber"},
        { "trigger": "go_back", "source": "setNumber", "dest": "setClock"},

        { "trigger": "advance","source": "setNumber","dest": "setNow","conditions": "is_going_to_setNow"},
        { "trigger": "go_back", "source": "setNow", "dest": "setNumber"},

        { "trigger": "advance","source": "setNumber","dest": "setTarget","conditions": "is_going_to_setTarget"},
        { "trigger": "go_back", "source": "setTarget", "dest": "setNumber"},
    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
#channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
#channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
#if channel_secret is None:
    #print("Specify LINE_CHANNEL_SECRET as environment variable.")
    #sys.exit(1)
#if channel_access_token is None:
    #print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    #sys.exit(1)

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

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        
        if(event.message.type=="postback" and machine.state=="book"):
            machine.set_setName_flag(event.postback.data)

        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        if (event.message.type=="text" and event.message.text=="返回")or check_go_back(machine.state, event):
            response = machine.go_back(event)
        elif machine.state=="clockCenter" and (event.message.text=="開始計時"):
            response = machine.cycle(event)
        else:
            response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    #port = os.environ.get("PORT", 8000)
    #port = os.environ['PORT']
    app.run()

