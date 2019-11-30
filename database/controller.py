from database.model import Model

class Controller():
    def __init__(self):
        self.db=Model()

    def save_location_info(self,info,timer):
        try:
            print("try to save data")
            query=self.db.read("name",info['spotName'])
            if query== None or len(query)==0:
                self.db.create(info,str(timer))
            return True
        except:
            return False