from llm.factory.training.training import Training
from langchain.schema import Document
import time
class TrainingSQL(Training):
    def __init__(self):
        super().__init__()
        self.columns = ['content','query','timecreated']
        self.context = 'training_sql'

    def save_training_data(self,data):

        try:

            documents = [
                Document(page_content=data['content'], metadata={"query": data['query'],"timecreated": int(time.time())})
            ]
            self.vector_db.add_vectordb(documents,self.context)

            return {'message': 'Success'}
        
        except:

            return {'message': 'Fail'}

    def check_training_duplication(self):
        pass