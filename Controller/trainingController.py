from langchain.schema import Document
from flask import jsonify
import pandas as pd
from config.config_vectordb import VectorDB
from datetime import datetime

vector_db = VectorDB()
def training_from_import(request):
    file = request.files['file']
    data = pd.read_excel(file)
    few_shots = {}
    create_date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    connect_rds = vector_db.connect_vectordb()
    for index, row in data.iterrows():
        if check_dup_data_training(row.question, connect_rds) == False:
            few_shots[row[0]] = row[1]
    documents = [
        Document(page_content=question, metadata={"query": few_shots[question], "date_create": create_date_time})
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

def check_dup_data_training(question, connect_rds):
    is_dup = False
    results = connect_rds.similarity_search_with_score(question, k=1, distance_threshold=0.1)
    if results != []:
        is_dup = True
    return is_dup