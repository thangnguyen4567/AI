from langchain.schema import Document
import pandas as pd
from config.config_vectordb import add_vectordb

def training_from_import(request):
    file = request.files['file']
    data = pd.read_excel(file)
    few_shots = {}
    for index, row in data.iterrows():
        few_shots[row[0]] = row[1]
    documents = [
        Document(page_content=question, metadata={"query": few_shots[question]})
        for question in few_shots.keys()
    ]
    add_vectordb(documents)
    return 'Import dữ liệu thành công'

