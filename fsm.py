from transitions.extensions import GraphMachine

from utils import send_text_message, send_template_message
from msg_pool import get_center_msg,get_set_clock_msg

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.timer={"min":0,"sec":0}

    # center
    def is_going_to_center(self,*arg):
        return True

    def on_enter_center(self, event):
        reply_token = event.reply_token
        send_template_message(reply_token, get_center_msg())

    def on_exit_center(self,ev):
        print("Leaving state1")

    # setClock
    def is_going_to_setClock(self, event):
        text = event.message.text
        print("開啟自訂計時\n")
        return text.lower() == "開啟自訂計時"


    def on_enter_setClock(self, event):
        reply_token = event.reply_token
        send_template_message(reply_token, get_set_clock_msg(self.timer))
        #self.go_back()

    def on_exit_setClock(self,*arg):
        print("Leaving state2")

    # setClock
    def is_going_to_setTime(self, event):
        text = event.message.text
        print("設定時間\n")
        return text.lower() == "設定時間"


    def on_enter_setTime(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入時間,例如3分12秒為「 3：12 」")
        #self.go_back()

    def on_exit_setTime(self,event):
        content=event.message.text.split(":")
        self.timer['min']=int(content[0])
        self.timer['sec']=int(content[1])    
        print(event.message.text.split(":"))
        print("Leaving state2")
