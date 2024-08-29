from abc import ABC, abstractmethod 
from tools.helper import remove_stopwords

class Context(ABC):
    def __init__(self):
        pass

    ##Lấy danh sách document theo context
    @abstractmethod
    def retriever_document(self,contextdata: dict,question: str) -> str:
        pass

    def aggregation_question_context(self,chat_history: list,question) -> str:
        
        aggregation = ''

        if chat_history is not None:
            for chat in chat_history[-3:]:
                if 'human' in chat:
                    aggregation += ' '+chat['human']

        aggregation += ' '+question

        return remove_stopwords(aggregation)