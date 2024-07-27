from config.config_vectordb import VectorDB
from llm.factory.context.context import Context
class ContextReport(Context):
    def __init__(self):
        self.prompt = "The user provides a question and you provide SQL. You will only respond with SQL code and not with any explanations.\n\nRespond with only SQL code. Do not answer with any explanations -- just the code.\n"
        self.schema_sql = {
            "text": [{"name": "query"}],
        }
        self.schema_ddl = {
            "text": [{"name": "table"}],
        }
        self.chat_history = []

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
    
    def retriever_document(self,contextdata: dict,question: str) -> str:
        ddl_list = self.get_similar_ddl(question)
        sql_list = self.get_similar_question_sql(question)

        for ddl in ddl_list:
            self.prompt += f"{ddl}\n\n"
        
        for sql in sql_list:
            if sql is None:
                print("example is None")
            else:
                if sql is not None and "question" in sql and "sql" in sql:
                    dict = {}
                    dict['human'] = sql["question"]
                    dict['bot'] = sql["sql"]
                    self.chat_history.append(dict)

        return self.prompt

    def get_similar_question_sql(self, question: str, **kwargs) -> list:
        return self._extract_documents(
            VectorDB().connect_vectordb(index_name='training_sql',index_schema=self.schema_sql).similarity_search(question,k=5)
        )

    def get_similar_ddl(self, question: str, **kwargs) -> list:
        return self._extract_documents(
            VectorDB().connect_vectordb(index_name='training_ddl',index_schema=self.schema_ddl).similarity_search(question,k=5)
        )