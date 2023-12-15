from langchain.schema import Document
from langchain.vectorstores import faiss
from langchain.embeddings import HuggingFaceHubEmbeddings
import pandas as pd
from langchain.vectorstores.redis import Redis

def config_vectordb():
    embeddings = HuggingFaceHubEmbeddings()
    data = pd.read_excel("./document/data.xlsx",usecols=['question', 'answer'])
    few_shots = {}
    for index, row in data.iterrows():
        few_shots[row[0]] = row[1]
    newDocs = [
        Document(page_content=question, metadata={"query": few_shots[question]})
        for question in few_shots.keys()
    ]

    vector_db = redis_vector(embeddings, newDocs)
    # vector_db = faiss.FAISS.from_documents(newDocs, embeddings)
    
    return vector_db


def redis_vector(embeddings, documents):
    redis_url = "redis://127.0.0.1:6380"
    index_name = 'rds_index'
    rds = Redis.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=index_name,
        redis_url=redis_url
    )
    return rds