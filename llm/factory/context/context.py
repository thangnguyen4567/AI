from abc import ABC, abstractmethod 
class Context(ABC):
    def __init__(self):
        pass

    ##Lấy danh sách document theo context
    @abstractmethod
    def retriever_document(self,contextdata: dict,question: str) -> str:
        pass