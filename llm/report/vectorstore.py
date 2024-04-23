from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from tools.helper import convert_unixtime
from langchain.vectorstores.redis import Redis
from dotenv import load_dotenv
import os
import time
import redis
from llm.report.base import LLMBase


class VectorStore(LLMBase):
    def __init__(self):
        LLMBase.__init__(self)
        load_dotenv()
        self.embeddings = OpenAIEmbeddings()
        self.vector_name = os.getenv("VECTORDB_NAME")
        self.vector_host = os.getenv("VECTORDB_HOST")
        self.vector_port = os.getenv("VECTORDB_PORT")
        self.redis_url = self.vector_name + '://' + self.vector_host + ':' + self.vector_port
        self.ddl_schema = {
            "text": [{"name": "table"}],
        }
        self.sql_schema = {
            "text": [{"name": "query"}],
        }

        # self.documentation_collection = Redis.from_existing_index(
        #     self.embeddings,
        #     index_name='training_ddl',
        #     redis_url=self.redis_url,
        #     schema=self.ddl_schema
        # )

        # self.ddl_collection = Redis.from_existing_index(
        #     self.embeddings,
        #     index_name='training_ddl',
        #     redis_url=self.redis_url,
        #     schema=self.ddl_schema
        # )

        # self.sql_collection = Redis.from_existing_index(
        #     self.embeddings,
        #     index_name='training_sql',
        #     redis_url=self.redis_url,
        #     schema=self.sql_schema
        # )

        self.client = redis.Redis(
            host=self.vector_host,
            port=self.vector_port,
        )

    @staticmethod
    def _extract_documents(query_results) -> list:
        if query_results is None:
            return []
        data = []
        for value in query_results:
            if 'query' in value.metadata:
                data.append({'question':value.page_content,'sql':value.metadata['query']})
            else :
                data.append(value.metadata['table'])

        return data

    def get_similar_question_sql(self, question: str, **kwargs) -> list:
        return self._extract_documents(
            self.sql_collection.similarity_search(query=question,k=10)
        )

    def get_related_ddl(self, question: str, **kwargs) -> list:
        return self._extract_documents(
            self.ddl_collection.similarity_search(query=question,k=10)
        )

    def get_related_documentation(self, question: str, **kwargs) -> list:
        return self._extract_documents(
            self.documentation_collection.similarity_search(query=question,k=10)
        )
    
    def add_question_sql(self, question: str, sql: str, **kwargs) -> str:
        if (self.sql_collection.similarity_search_with_score(question, k=1, distance_threshold=0.1) != []):
            documents = [
                Document(page_content=question, metadata={"query": sql,"timecreated": int(time.time())})
            ]
            self.sql_collection.aadd_documents(documents)

    def add_ddl(self, table: str, ddl: str, **kwargs) -> str:
        if (self.sql_collection.similarity_search_with_score(table, k=1, distance_threshold=0.1) != []):
            documents = [
                Document(page_content=table, metadata={"table": ddl,"timecreated": int(time.time())})
            ]
            self.sql_collection.aadd_documents(documents)

    def add_documentation(self, documentation: str, **kwargs) -> str:
        if (self.sql_collection.similarity_search_with_score(documentation, k=1, distance_threshold=0.1) != []):
            documents = [
                Document(page_content=documentation, metadata={"timecreated": int(time.time())})
            ]
            self.sql_collection.aadd_documents(documents)
    
    def get_training_ddl(self, **kwargs) -> list:
        data = []
        for key in self.client.scan_iter("doc:training_ddl*"):
            content = self.client.hget(key,'content')
            table = self.client.hget(key,'table')
            timecreated = self.client.hget(key,'timecreated')
            data.append({
                        'id':key.decode(),
                        'content':content.decode(),
                        'answer':table.decode(),
                        'timecreated': convert_unixtime(timecreated),
                        'type': 'training_ddl'
                        })
        return sorted(data, key=lambda x: x['timecreated'],reverse=True)

    def get_training_sql(self, **kwargs) -> list:
        data = []
        for key in self.client.scan_iter("doc:training_ddl*"):
            content = self.redis_client.hget(key,'content')
            query = self.redis_client.hget(key,'query')
            timecreated = self.redis_client.hget(key,'timecreated')

            data.append({
                        'id':key.decode(),
                        'content':content.decode(),
                        'answer':query.decode(),
                        'timecreated': convert_unixtime(timecreated),
                        'type': 'training_ddl'
                        })
        return sorted(data, key=lambda x: x['timecreated'],reverse=True)

    def delete_training_data(self,key, **kwargs) -> bool:
        self.client.delete(key)
    
    def update_training_data(self,data):
        key = data['id']
        obj = {}  
        if(data['type'] == 'training_sql'):
            obj['query'] = data['answer']
        elif (data['type'] == 'training_ddl'):         
            obj['table'] = data['answer']
        obj['content'] = data['content']
        obj['timecreated'] = int(time.time())
        self.client.hmset(key,obj)

    