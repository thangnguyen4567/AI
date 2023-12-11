from langchain.schema import Document
from langchain.vectorstores import faiss
from langchain.embeddings import HuggingFaceHubEmbeddings
import pandas as pd
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
    vector_db = faiss.FAISS.from_documents(newDocs, embeddings)
    return vector_db