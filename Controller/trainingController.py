from langchain.schema import Document
from flask import jsonify
import pandas as pd
from config.config_vectordb import VectorDB
import time

vector_db = VectorDB()
connect_rds = vector_db.connect_vectordb()
def training_from_import(request):
    result = {'message': 'Import dữ liệu thành công'}
    if 'file' not in request.files:
        return {'message': 'No file part'}
    file = request.files['file']
    data = pd.read_excel(file)
    few_shots = {}
    documents = None
    for index, row in data.iterrows():
        few_shots[row[0]] = row[1]
        if check_dup_data_training(row.question, connect_rds) == False:
            few_shots[row[0]] = row[1]
            documents = [
                Document(page_content=question, metadata={"query": few_shots[question],"timecreated":  int(time.time()) })
                for question in few_shots.keys()
            ]
    if documents is not None:
        vector_db.add_vectordb(documents)
    else:
        result = {'message': 'Import dữ liệu không thành công'}
    return result

def training_from_api(request):
    requestJson = request.get_json()
    question = requestJson['question']
    query = requestJson['query']
    if check_dup_data_training(question, connect_rds) == False:
        documents = [
            Document(page_content=question, metadata={"query": query,"timecreated": int(time.time())})
        ]
        vector_db.add_vectordb(documents)
        result = {'message': 'Import dữ liệu thành công'}
    else: result = {'message': 'Import dữ liệu trùng'}
    return result

def training_from_query(request):
    data = request.form
    question = data['question']
    query = data['answer']
    if check_dup_data_training(question, connect_rds) == False:
        documents = [
            Document(page_content=question, metadata={"query": query,"timecreated": int(time.time())})
        ]
        vector_db.add_vectordb(documents)
        result = {'message': 'Import dữ liệu thành công'}
    else: result = {'message': 'Import dữ liệu trùng'}
    return result

def check_dup_data_training(question, connect_rds):
    is_dup = False
    results = connect_rds.similarity_search_with_score(question, k=1, distance_threshold=0.1)
    if results != []:
        is_dup = True
    return is_dup