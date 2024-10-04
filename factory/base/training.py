from config.config_vectordb import VectorDB
from config.config_sqldb import SQLDB
from abc import ABC, abstractmethod 

class Training(ABC):
    def __init__(self):
        self.redis_client = VectorDB().connect_client()
        self.vector_db = VectorDB()
        # self.sql_db = SQLDB()
        self.reponse = {
            'error': False,
            'message': ''
        }

    @abstractmethod
    def save_training_data(self):
        pass

    @abstractmethod
    def check_training_duplication(self):
        pass
    
    def update_training_data(self,data) -> dict:

        try:
            obj = {}  

            for value in data:
                obj[value] = data[value]
            
            self.redis_client.hmset(data['id'],obj)

            self.reponse['message'] = 'Sửa thành công'

        except:
            self.reponse['message'] = 'Sửa thất bại'

        return self.reponse
        
    def get_training_data(self,index) -> list:
        
        data = []

        for key in self.redis_client.scan_iter("doc:"+index+"*"):
            obj = {}
            obj['id'] = key.decode()
            for column in self.columns:
                content = self.redis_client.hget(key,column)
                obj[column] = content.decode() if content else 'None'
            data.append(obj)

        return data
    
    def delete_training_data(self,key,data) -> dict:

        try:
            self.redis_client.delete(key)

            self.reponse['message'] = 'Xóa thành công'

        except:
            self.reponse['message'] = 'Xóa thất bại'

        return self.reponse