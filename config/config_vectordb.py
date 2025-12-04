from langchain_openai import OpenAIEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore
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

        config = RedisConfig(
            index_name=index_name,
            redis_url=self.redis_url,
            metadata_schema=index_schema,
        )
 
        vector_store = RedisVectorStore(self.embeddings, config=config)
        return vector_store

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
    
    def get_list_index(self):
        index_list = self.connect_client().execute_command('FT._LIST')
        data = []
        for index in index_list:
            data.append(index.decode())
        return data
