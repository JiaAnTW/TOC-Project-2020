import pymysql
import os
import datetime

class Model():
    def __init__(self):
        try:
            self.db = pymysql.connect("localhost",os.environ['USER'],os.environ['DATABASE_PASSWORD'],os.environ['DATABASE'] )
            print("database connection success")
        except:
            print("database connection fail")
            exit(1)

    def index(self):
        try:
            cursor = self.db.cursor()
        except:
            self._reconnect()
            cursor = self.db.cursor()
            
        try:
            query = "SELECT * FROM pin"
            cursor.execute(query)
            data = cursor.fetchone()
            print ("data is "+str(data))
        except:
            print("Error when query [index]")

    
    def create(self,newSpot,timer):
        try:
            cursor = self.db.cursor()
        except:
            self._reconnect()
            cursor = self.db.cursor()
        try:
            print("try to create "+str(newSpot))    
            query = "INSERT INTO pin(name,address, latitude, longitude) VALUES('%s', '%s', %f,%f)"% \
                (newSpot['spotName'], newSpot['address'], newSpot['latitude'], newSpot['longitude'])
            print("query is "+query)
            cursor.execute(query)
        except Exception as e:
            print("Error when query [create_location]")
            print(e)
        try:
            query = "SELECT id FROM pin WHERE name='%s'"% (newSpot['spotName'])
            cursor.execute(query)
            data = cursor.fetchone()
            print("data is "+str(data))
            self.create_table(data[0],timer)
            self.db.commit()
        except Exception as e:
            print("Error when query [send_create_table]")
            print(e)
        


    def read(self,data_type,target):
        try:
            cursor = self.db.cursor()
        except:
            self._reconnect()
            cursor = self.db.cursor()
            
        try:
            query = "SELECT * FROM pin WHERE %s = '%s'"%(data_type,target)
            cursor.execute(query)
            data = cursor.fetchone()
            if data!=None:
                print ("data is "+str(data))
            return data
        except:
            print("Error when query [index]")


    def update(self,newSpot):
        try:
            cursor = self.db.cursor()
        except:
            self._reconnect()
            cursor = self.db.cursor()
        #try:    
        query = "UPDATE pin SET name='%s', address='%s'\
                ,latitude=%f, longitude=%f "% \
                (newSpot['spotName'], newSpot['address'], newSpot['latitude'], newSpot['longitude'])
        #except:
        #print("Error when query [update_location]")
        cursor.execute(query)

    def create_table(self,id,time):
        try:
            cursor = self.db.cursor()
        except:
            self._reconnect()
            cursor = self.db.cursor()
        
        try:
            query = "CREATE TABLE spot_"+str(id)+" (time TEXT NOT NULL, period TEXT NOT NULL) ENGINE=InnoDB  DEFAULT CHARSET=utf8"
            cursor.execute(query)
            self.db.commit()
        except Exception as e:
            print("Error when query [create_table]")
            print(e)
        try:
            now=datetime.datetime.now() 
            localtime = now.strftime("%Y-%m-%d-%a %H:%M:%S")
            query = "INSERT INTO spot_"+str(id)+" (time,period) VALUES('%s', '%s')"% \
            (localtime,time)
            print("query is "+query)
            cursor.execute(query)
            self.db.commit()
        except Exception as e:
            print("Error when query [create_table]")
            print(e)




    
    def _reconnect(self):
        try:
            self.db = pymysql.connect(os.environ['DB_IP'],os.environ['USER'],os.environ['DATABASE_PASSWORD'],os.environ['DATABASE'] )
        except:
            print("Reconnect database fail, program stop")
            exit(1)


    def __del__(self):
        self.db.close()