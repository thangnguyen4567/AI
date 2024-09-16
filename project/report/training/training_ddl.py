from factory.base.training import Training
from langchain.schema import Document
import time
class TrainingDDL(Training):
    def __init__(self):
        super().__init__()
        self.columns = ['content','table','timecreated']
        self.context = 'training_ddl'

    def save_training_data(self,data):
        try:
            documents = [
                Document(page_content=data['content'], metadata={"table": data['table'],"timecreated": int(time.time())})
            ]
            self.vector_db.add_vectordb(documents,self.context)

            return {'message': 'Success'}
        
        except:

            return {'message': 'Success'}

    def check_training_duplication(self):
        pass