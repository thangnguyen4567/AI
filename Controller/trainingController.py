from langchain.schema import Document
from flask import jsonify
import pandas as pd
from config.config_vectordb import VectorDB
import time
import datetime
vector_db = VectorDB()
class TrainingController:
    def __init__(self):
        self.redis_client = vector_db.connect_client()
        
    def process_import(self,request):
        file = request.files['file']
        type = request.form['typedata']
        data = pd.read_excel(file)
        few_shots = {}
        for index, row in data.iterrows():
            few_shots[row[0]] = row[1]
        for content in few_shots.keys():
            self.save_training_data(content,few_shots[content],type)
        return {'message': 'Import dữ liệu thành công'}

    def process_create(self,request):
        requestJson = request.get_json()
        self.save_training_data(requestJson['question'],requestJson['query'],'training_sql')
        return {'message': 'Import dữ liệu thành công'}

    def save_training_data(self,content,answer,type):
        if self.check_training_duplication(content,type) == False:
            if(type == 'training_sql'):
                    documents = [
                        Document(page_content=content, metadata={"query": answer,"timecreated": int(time.time())})
                    ]
                    vector_db.add_vectordb(documents,type)
            elif(type == 'training_ddl'):
                documents = [
                    Document(page_content=content, metadata={"table": answer,"timecreated": int(time.time())})
                ]
                vector_db.add_vectordb(documents,type)

    def get_training_data(self):
        data = []
        for key in self.redis_client.scan_iter("doc:*"):
            obj = {}
            content = self.redis_client.hget(key,'content')
            query = self.redis_client.hget(key,'query')
            timecreated = self.redis_client.hget(key,'timecreated')
            obj['id'] = key.decode()
            obj['question'] = content.decode() if content else 'None'
            obj['answer'] = query.decode() if query else 'None'
            obj['timecreated'] = datetime.datetime.utcfromtimestamp(int(timecreated.decode())).strftime("%d/%m/%Y %H:%M") if timecreated else '20/12/2023 00:00'
            # obj['action'] = '<a class="delete btn btn-danger" id="'+obj['id']+'">Xóa</a>'
            data.append(obj)
        sorted_data = sorted(data, key=lambda x: x['timecreated'],reverse=True)
        return sorted_data
    
    def delete_training_data(self,id):
        self.redis_client.delete(id)
        return {'message': 'Xóa thành công'}
    
    def check_training_duplication(self,question,type):
        is_dup = False
        if(self.redis_client.exists(type)):
            redis_vectordb = vector_db.connect_vectordb(type)
            results = redis_vectordb.similarity_search_with_score(question, k=1, distance_threshold=0.1)
            if results != []:
                is_dup = True
        return is_dup