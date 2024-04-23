from abc import ABC, abstractmethod

class LLMBase(ABC):
    def __init__(self, config=None):
        self.config = config
        self.run_sql_is_set = False

    def generate_sql(self, question: str, **kwargs) -> str:
        question_sql_list = self.get_similar_question_sql(question, **kwargs)
        ddl_list = self.get_related_ddl(question, **kwargs)
        # doc_list = self.get_related_documentation(question, **kwargs)
        prompt = self.get_sql_prompt(
            question=question,
            question_sql_list=question_sql_list,
            ddl_list=ddl_list,
            doc_list='',
            **kwargs,
        )
        llm_response = self.submit_prompt(prompt, **kwargs)
        return llm_response
    
    @abstractmethod
    def get_similar_question_sql(self, question: str, **kwargs) -> list:
        pass
    
    @abstractmethod
    def get_related_ddl(self, question: str, **kwargs) -> list:
        pass

    @abstractmethod
    def get_related_documentation(self, question: str, **kwargs) -> list:
        pass
    
    @abstractmethod
    def get_sql_prompt(
        self,
        question: str,
        question_sql_list: list,
        ddl_list: list,
        doc_list: list,
        **kwargs,
    ):
        pass

    @abstractmethod
    def submit_prompt(self, prompt, **kwargs) -> str:
        pass

    @abstractmethod
    def add_question_sql(self, question: str, sql: str, **kwargs) -> str:
        pass

    @abstractmethod
    def add_ddl(self, ddl: str, table: str, **kwargs) -> str:
        pass

    @abstractmethod
    def add_documentation(self, documentation: str, **kwargs) -> str:
        pass

    @abstractmethod
    def get_training_ddl(self, **kwargs) -> list:
        pass
    
    @abstractmethod
    def get_training_sql(self, **kwargs) -> list:
        pass

    @abstractmethod
    def delete_training_data(self,id: str, **kwargs) -> bool:
        pass

    @abstractmethod
    def update_training_data(id: str, **kwargs) -> bool:
        pass