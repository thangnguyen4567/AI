from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.vectorstores.redis import Redis
from dotenv import load_dotenv
import os

class VectorDB:
    def __init__(self):
        load_dotenv()
        self.embeddings = HuggingFaceHubEmbeddings()
        self.redis_url = os.getenv("VECTORDB_NAME") + '://' + os.getenv("VECTORDB_HOST") + ':' + os.getenv("VECTORDB_PORT")
        self.index_name = 'trainingreport'
        self.index_schema = {
            "text": [{"name": "query"}],
        }

    def connect_vectordb(self):
        vector_db = Redis.from_existing_index(
            self.embeddings,
            index_name=self.index_name,
            redis_url=self.redis_url,
            schema=self.index_schema
        )
        return vector_db

    def add_vectordb(self, documents):
        Redis.from_documents(
            documents=documents,
            embedding=self.embeddings,
            index_name=self.index_name,
            redis_url=self.redis_url
        )