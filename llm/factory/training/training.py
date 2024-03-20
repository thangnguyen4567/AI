from config.config_vectordb import VectorDB
from config.config_sqldb import SQLDB
from abc import ABC, abstractmethod 
vector_db = VectorDB()
class Training(ABC):
    def __init__(self):
        self.redis_client = vector_db.connect_client()
        self.vector_db = vector_db
        self.sql_db = SQLDB()

    @abstractmethod
    def save_training_data(self):
        pass

    @abstractmethod
    def delete_training_data():
        pass

    @abstractmethod
    def update_training_data(self):
        pass

    @abstractmethod
    def check_training_duplication(self):
        pass
    
    def get_training_data(self) -> list:
        data = []
        for key in self.redis_client.scan_iter("doc:"+self.context+"*"):
            obj = {}
            obj['id'] = key.decode()
            for column in self.columns:
                content = self.redis_client.hget(key,column)
                obj[column] = content.decode() if content else 'None'
            data.append(obj)
        return data
    
    def delete_training_data(self,key):
        self.redis_client.delete(key)
        return {'message': 'Xóa thành công'}
