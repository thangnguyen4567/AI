from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain.vectorstores.redis import Redis
from dotenv import load_dotenv
import os
import redis
class VectorDB:
    def __init__(self):
        load_dotenv()
        self.embeddings = OpenAIEmbeddings()
        # self.embeddings = HuggingFaceHubEmbeddings()
        self.vector_name = os.getenv("VECTORDB_NAME")
        self.vector_host = os.getenv("VECTORDB_HOST")
        self.vector_port = os.getenv("VECTORDB_PORT")
        self.redis_url = self.vector_name + '://' + self.vector_host + ':' + self.vector_port

    def connect_vectordb(self, index_name, index_schema):
        vector_db = Redis.from_existing_index(
            self.embeddings,
            index_name=index_name,
            redis_url=self.redis_url,
            schema=index_schema
        )
        return vector_db

    def add_vectordb(self, documents, index_name):
        Redis.from_documents(
            documents=documents,
            embedding=self.embeddings,
            index_name=index_name,
            redis_url=self.redis_url
        )
    def connect_client(self):
        redis_client = redis.Redis(
            host=self.vector_host,
            port=self.vector_port,
        )
        return redis_client