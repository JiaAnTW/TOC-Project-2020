from transitions.extensions import GraphMachine
import datetime
import threading
from database.controller import Controller as DB
from utils import *
from msg_pool import *


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.timer=datetime.timedelta(hours=0,minutes = 0, seconds = 0)
        self.number={"now":0,"target":0}
        self.clock={"set":False, "time":datetime.timedelta(minutes = 0, seconds = 0),"start":datetime.datetime.now()}
        self.threadPool=[]
        self.clockPool=[]
        self.setNameFlag=-1
        self.index=0
        self.beforeState="none"
        self.DB=DB()

    def set_setName_flag(self,i):
        self.setNameFlag=int(i)
        print("Now fous on "+str(self.setNameFlag))
    
    def get_name_by_index(self,index):
        for clockInfo in self.clockPool:
            if clockInfo['index']==index:
                return clockInfo['name']
        return None

    def delete_clock_from_pool(self,index):
        i=0
        for clock in self.clockPool:
            if clock['index']==index:
                self.clockPool.pop(i)
                return
            i=i+1


    # center
    def is_going_to_center(self,*arg):
        return True

    def on_enter_center(self, event):
        reply_token = event.reply_token
        send_template_message(reply_token, get_center_msg())

    def on_exit_center(self,event):
        self.set_setName_flag(-1)
        print("Leaving state1")

    def is_back_to_center(self, event):
        return self.setNameFlag==-1

    # setClock
    def is_going_to_setClock(self, event):
        text = event.message.text
        print(event.message.text)
        return (text.lower() == "開啟自訂計時"or text.lower() == "修改號碼牌內容")

    def on_enter_setClock(self, event):
        print("setNameFlag is "+str(self.setNameFlag))
        reply_token = event.reply_token
        if(self.setNameFlag!=-1):
            self.timer=self.clockPool[self.setNameFlag]['timer']
            self.number=self.clockPool[self.setNameFlag]['number']
            self.clock=self.clockPool[self.setNameFlag]['clock']
            self.index=self.clockPool[self.setNameFlag]['index']
        send_template_message(reply_token, get_set_clock_msg(self.timer,self.number))
        #self.go_back()

    def on_exit_setClock(self,event):
        print("setNameFlag is "+str(self.setNameFlag))
        if(event.message.text=="確定送出"):
            msg="設定完成!輪到你的時候會用訊息通知你歐~現在可以再設定新的計時器"
            active_send_text_msg(event.source.user_id,msg,datetime.timedelta(hours=0,minutes = 0, seconds = 0),self.number)
            self.clock['start']=datetime.datetime.now()
            self.clockPool.append({
                'timer':self.timer,
                'number':self.number,
                'clock':self.clock,
                'index':self.index,
                'name': None,
                'spotName':None,
                'locationInfo':None
            })
            tmp=threading.Thread(
                target =  active_send_clock_msg, 
                args = (
                    event.source.user_id,
                    " 快要排到了歐!",
                    self.clockPool[len(self.clockPool)-1]['timer'],
                    self.clockPool[len(self.clockPool)-1]['number'],
                    self.index,
                    self.delete_clock_from_pool,
                    self.get_name_by_index
                )
            )
            tmp.start()
            self.threadPool.append(tmp)
            
            isRepeat= False
            for i in range(4):
                for clock in self.clockPool:
                    if(clock['index']==i):
                        isRepeat=True
                        break
                if isRepeat==False:
                    self.index=i
                    break
            self.timer=datetime.timedelta(hours=0,minutes = 0, seconds = 0)
            self.number={"now":0,"target":0}
            self.clock={"set":False, "time":datetime.timedelta(minutes = 0, seconds = 0)}
        print("Leaving state2")
        return
    
    # setTime
    def is_going_to_setTime(self, event):
        text = event.message.text
        print("直接輸入時間\n")
        return text.lower() == "直接輸入時間"


    def on_enter_setTime(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入時間,例如3分12秒為「 3：12 」")
        #self.go_back()

    def on_exit_setTime(self,event):
        content=event.message.text.split(":")
        self.timer=datetime.timedelta(hours=0,minutes = int(content[0]), seconds = int(content[1]))
        print(event.message.text.split(":"))
        print("Leaving state2")

    #clockCenter
    def is_going_to_clockCenter(self, event):
        text = event.message.text
        print("enter cycle\n")
        return text.lower() == "設定時間"

    def cycle_in_clockCenter(self, event):
        text = event.message.text
        date = datetime.datetime.now()
        self.clock['set']=True
        self.clock['time']=datetime.timedelta(hours=date.hour,minutes = date.minute, seconds = date.second)
        return text.lower() == "開始計時"


    def on_enter_clockCenter(self, event):
        reply_token = event.reply_token
        send_template_message(reply_token, get_set_clockCenter_msg(self.timer,self.clock["set"]))
        #self.go_back()

    def on_exit_clockCenter(self,event):
        if event.message.text =="結束計時":
            date = datetime.datetime.now()
            tmp = self.clock['time']
            self.clock['time']=datetime.timedelta(hours=date.hour,minutes = date.minute, seconds = date.second)-tmp
            self.clock['set']=False
            self.timer=self.clock['time']
        print("Leaving clockCenter")

    #setNumber

    def is_going_to_setNumber(self, event):
        text = event.message.text
        print("設定號碼牌\n")
        return text.lower() == "設定號碼牌"


    def on_enter_setNumber(self, event):
        reply_token = event.reply_token
        send_template_message(reply_token, get_set_number_msg(self.number))
        #self.go_back()

    def on_exit_setNumber(self,event):
        print("Leaving setNumber")


    def is_going_to_setTarget(self, event):
        text = event.message.text
        print("設定你的號碼\n")
        return text.lower() == "設定你的號碼"


    def on_enter_setTarget(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您的號碼（阿拉伯數字）")
        #self.go_back()

    def on_exit_setTarget(self,event):
        if int( event.message.text) < self.number['now']:
            msg="你的號碼牌不能比現在的號碼小啦~請重新輸入歐！"
            active_send_text_msg(event.source.user_id,msg,datetime.timedelta(hours=0,minutes = 0, seconds = 0),self.number)
        else:
            self.number['target']=int( event.message.text)
        print("Leaving setTarget")
    
    def is_going_to_setNow(self, event):
        text = event.message.text
        print("設定目前號碼\n")
        return text.lower() == "設定目前號碼"

    def on_enter_setNow(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入目前的號碼（阿拉伯數字）")
        #self.go_back()

    def on_exit_setNow(self,event):
        if self.number['target']>0 and int( event.message.text) > self.number['target']:
            msg="現在的號碼牌不能比你的號碼大啦~請重新輸入歐！"
            active_send_text_msg(event.source.user_id,msg,datetime.timedelta(hours=0,minutes = 0, seconds = 0),self.number)
        else:
            self.number['now']=int( event.message.text)  
        print("Leaving setNow")

    def is_going_to_book(self, event):
        text = event.message.text
        print("查看目前計時器\n")
        return text.lower() == "查看目前計時器"

    def on_enter_book(self, event):
        reply_token = event.reply_token
        self.setNameFlag=-1
        if len(self.clockPool)>0:
            send_template_message(reply_token, get_book_msg(self.clockPool))
        else:
            msg="目前沒有任何計時器歐"
            active_send_text_msg(event.source.user_id,msg,datetime.timedelta(hours=0,minutes = 0, seconds = 0),self.number)
            self.go_back(event)

    def on_exit_book(self,event):
        print("Leaving book")
    
    def is_back_to_book(self, event):
        ans= False
        print("setNameFlag is "+str(self.setNameFlag))
        if self.setNameFlag != -1:
            ans = True
        return ans

    def is_going_to_setName(self, event):
        text = event.message.text
        print("更改計時器名稱\n")
        return text.lower() == "更改計時器名稱"

    def on_enter_setName(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請傳給我計時器的新名稱~")

    def on_exit_setName(self,event):
        self.clockPool[self.setNameFlag]['name']=event.message.text
        self.setNameFlag=-1
        print("Leaving setName")

    def is_going_to_locationCenter(self, event):
        text = event.message.text
        print("enter cycle\n")
        return text.lower() == "輸入位置資訊"

    def on_enter_locationCenter(self, event):
        reply_token = event.reply_token
        index=self.setNameFlag
        send_template_message(reply_token, get_locationCenter_msg(self.clockPool[index]['spotName'],self.clockPool[index]['locationInfo']))
        #self.go_back()

    def on_exit_locationCenter(self,event):
        if(event.message.text.lower()=='返回'):
            output=self.clockPool[self.setNameFlag]['locationInfo']
            output['spotName']=self.clockPool[self.setNameFlag]['spotName']
            self.DB.save_location_info(output)
        print("Leaving locationCenter")
    
    def is_going_to_setSpotName(self, event):
        text = event.message.text
        print("輸入地點名稱\n")
        return text.lower() == "輸入地點名稱"

    def on_enter_setSpotName(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入該地點的名稱~")

    def on_exit_setSpotName(self,event):
        self.clockPool[self.setNameFlag]['spotName']=event.message.text
        print("Leaving 輸入地點名稱")

    def is_going_to_setLocationInfo(self, event):
        text = event.message.text
        print("回傳地理資訊\n")
        return text.lower() == "回傳地理資訊"

    def on_enter_setLocationInfo(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "回傳該地點的地理資訊~")

    def on_exit_setLocationInfo(self,event):
        self.clockPool[self.setNameFlag]['locationInfo']={
            'address': event.message.address,
            'latitude':event.message.latitude,
            'longitude':event.message.longitude
        }
        print("Leaving 輸入地理資訊")