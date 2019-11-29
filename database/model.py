import pymysql

class Model():
    def __init__(self):
        try:
            self.db = pymysql.connect("localhost","waku","0000","waku" )
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

    
    def create(self,newSpot):
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
            self.db.commit()
        except:
            print("Error when query [create_location]")
        


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



    
    def _reconnect(self):
        try:
            self.db = pymysql.connect("localhost","waku","0000","waku" )
        except:
            print("Reconnect database fail, program stop")
            exit(1)


    def __del__(self):
        self.db.close()

#test=Model()
#test.index()