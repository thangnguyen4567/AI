from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.vectorstores.redis import Redis
from dotenv import load_dotenv
load_dotenv()
import os
embeddings = HuggingFaceHubEmbeddings()
redis_url =  os.getenv("VECTORDB_NAME")+'://'+os.getenv("VECTORDB_HOST")+':'+os.getenv("VECTORDB_PORT")
index_name = 'trainingreport'
index_schema = {
    "text": [{"name": "query"}],
}
def connect_vectordb():
    vector_db = Redis.from_existing_index(
        embeddings,
        index_name=index_name,
        redis_url=redis_url,
        schema=index_schema
    )
    return vector_db

def add_vectordb(documents):
    Redis.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=index_name,
        redis_url=redis_url
    )