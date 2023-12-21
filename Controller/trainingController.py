from langchain.schema import Document
from flask import jsonify
import pandas as pd
from config.config_vectordb import VectorDB
import time
vector_db = VectorDB()
def training_from_import(request):
    file = request.files['file']
    data = pd.read_excel(file)
    few_shots = {}
    for index, row in data.iterrows():
        few_shots[row[0]] = row[1]
    documents = [
        Document(page_content=question, metadata={"query": few_shots[question],"timecreated":  int(time.time()) })
        for question in few_shots.keys()
    ]
    vector_db.add_vectordb(documents)
    result = {'message': 'Import dữ liệu thành công'}
    return result

def training_from_api(request):
    requestJson = request.get_json()
    question = requestJson['question']
    query = requestJson['query']
    documents = [
        Document(page_content=question, metadata={"query": query})
    ]
    vector_db.add_vectordb(documents)
    result = {'message': 'Import dữ liệu thành công'}
    return result
