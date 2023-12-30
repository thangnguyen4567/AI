from langchain.schema import Document
from flask import jsonify
from config.config_vectordb import VectorDB
from tools.helper import convert_unixtime
import pandas as pd
import time
import pyodbc
import re
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

    def get_training_sql(self):
        data = []
        for key in self.redis_client.scan_iter("doc:training_sql*"):
            obj = {}
            content = self.redis_client.hget(key,'content')
            query = self.redis_client.hget(key,'query')
            timecreated = self.redis_client.hget(key,'timecreated')
            obj['id'] = key.decode()
            obj['content'] = content.decode() if content else 'None'
            obj['answer'] = query.decode() if query else 'None'
            obj['timecreated'] = convert_unixtime(timecreated) if timecreated else '20/12/2023 00:00'
            obj['type'] = 'training_sql'
            data.append(obj)
        sorted_data = sorted(data, key=lambda x: x['timecreated'],reverse=True)
        return sorted_data
    
    def get_training_ddl(self):
        data = []
        for key in self.redis_client.scan_iter("doc:training_ddl*"):
            obj = {}
            content = self.redis_client.hget(key,'content')
            table = self.redis_client.hget(key,'table')
            timecreated = self.redis_client.hget(key,'timecreated')
            obj['id'] = key.decode()
            obj['content'] = content.decode() if content else 'None'
            obj['answer'] = table.decode() if table else 'None'
            obj['timecreated'] = convert_unixtime(timecreated) if timecreated else '20/12/2023 00:00'
            obj['type'] = 'training_ddl'
            data.append(obj)
        sorted_data = sorted(data, key=lambda x: x['timecreated'],reverse=True)
        return sorted_data
    
    def delete_training_data(self,request):
        key = request.form['id']
        self.redis_client.delete(key)
        return {'message': 'Xóa thành công'}

    def update_training_data(self,request):
        key = request.form['id']
        obj = {}
        obj['content'] = request.form['content']
        if(request.form['type'] == 'training_sql'):
            obj['query'] = request.form['answer']
        else:
            obj['table'] = request.form['answer']
        obj['timecreated'] = int(time.time())
        self.redis_client.hmset(key,obj)
        return {'message': 'Cập nhật thành công'}
    
    def create_training_data(self,request):
        if(request.form):
            data = request.form
            self.save_training_data(data['content'],data['answer'],data['type'])
        else:
            data = request.get_json()
            self.save_training_data(data['question'],data['query'],'training_sql')
        return {'message': 'Import dữ liệu thành công'}
    
    def check_training_duplication(self,question,type):
        is_dup = False
        if(self.redis_client.exists(type)):
            redis_vectordb = vector_db.connect_vectordb(type)
            results = redis_vectordb.similarity_search_with_score(question, k=1, distance_threshold=0.1)
            if results != []:
                is_dup = True
        return is_dup

    def generate_table_ddl(self,request):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server=103.127.207.180,3968;Database=EBM_TEST_QC;UID=ebm;PWD=4OcDQ4OLo5eGngU', autocommit=True)
        strings = request.get_json()['tables']
        tables = re.split(',', strings)
        cursor = conn.cursor()
        for table in tables:
            data = []
            for row in cursor.columns(table=table):
                data.extend([row])
                sql_template = "CREATE TABLE {} (\n{})"

                columns = []
                for entry in data:
                    column_definition = "{} {}({})".format(entry[3], entry[5], entry[7])
                    columns.append(column_definition)

                sql_columns = ",\n".join(columns)
                sql_statement = sql_template.format(table, sql_columns)
            self.save_training_data(table, sql_statement,'training_ddl')
