from database.model import Model
from pytrends.request import TrendReq
import random
import json
import time
import numpy as np

class Controller():
    def __init__(self):
        self.db=Model()

    def save_location_info(self,info,timer):
        try:
            print("try to save data")
            query=self.db.read("name",info['spotName'])
            if query== None or len(query)==0:
                id=self.db.create(info)
                self.db.create_table(id,str(timer))
            else:
                print("data is "+str(query))
                if(self.check_if_fake(query[0],str(timer),query[1])==True):
                    print("It is true!")
                    self.db.update(query[0],info)
                    self.db.create_spot_info(query[0],str(timer))
            return True
        except:
            return False
    
    def check_if_fake(self,id,get_time,name):
        print("ckeck if it is fake")
        lists=self.db.read_table(id)
        if len(lists)>3:
            box=0
            arr=[]
            timer=0
            k=3600
            tmp=0
            print("preprocessing")
            clock=get_time.split(":")
            for i in range(3):
                timer+=int(clock[i])*k
                k=k/60
            print("get time is "+str(timer))
            for data in lists:
                clock=data[1].split(":")
                k=3600
                tmp=0
                for i in range(3):
                    box+=int(clock[i])*k
                    tmp+=int(clock[i])*k
                    k=k/60
                print("add "+str(tmp)+"sec")
                arr.append(tmp)
            std=np.std(arr,ddof=1)
            mean=box/len(lists)
            if timer>(mean+2*std):
                if self.googleTrends(name,1)== False:
                    print("It is true!")
                    return False
            elif timer<(mean-2*std):
                if self.googleTrends(name,-1)== False:
                    print("It is true!")
                    return False
        return True

    def send_request(self,pytrend,period=3):
        try:
            print("Build sucess! Wait"+str(period)+"s to query")
            for i in range(period):
                print("#", end='') 
                time.sleep(1)
            return json.loads(pytrend.interest_over_time().to_json(orient='table'))['data']
        except:
            print("Fail! Wait"+str(period)+"s to query")
            self.send_request(pytrend,2*period)


    def googleTrends(self,target, isPos):
        pytrend = TrendReq(hl='en-US', tz=360)
        targetList=[target]
        try:
            print("try build")
            pytrend.build_payload(targetList,cat=0,timeframe='now 7-d',geo="TW",gprop='')
            preload =self.send_request(pytrend,random.randint(3,7))
            arr=[]
            timeCollect=[]
            size=len(preload)
            for i in range(4):
                index=preload[size-i-1]["date"].find("T")
                hr=preload[size-i-1]["date"][index+1]+preload[size-i-1]["date"][index+2]
                print("hour is "+hr)
                timeCollect.append(hr)
            for i in range(len(preload)-3):
                index=preload[i]["date"].find("T")
                for element in timeCollect:
                    if preload[i]["date"].find(element,index+1)!=-1:
                        print("日期："+str(preload[i]["date"]), "流量："+str(preload[i][target]))
                        arr.append(preload[i][target])
            print("==================================================")
            std=np.std(arr,ddof=1)
            mean=sum(arr)/len(arr)
            check_arr=[preload[len(preload)-3][target],preload[len(preload)-2][target],preload[len(preload)-1][target]]
            check_mean=sum(check_arr)/len(check_arr)
            if isPos==1 and check_mean>mean+2*std:
                return True
            elif isPos==-1 and check_mean<mean-2*std:
                return True
            return False
        except Exception as e:
            print(e)

