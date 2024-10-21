from factory.model_factory import ModelFactory
from abc import ABC, abstractmethod 

class Services(ABC):

    def __init__(self,config):

        self.question = config.get('question','test')
        self.chat_history = config.get('chat_history')
        self.contextdata = config.get('contextdata')
        self.context = config.get('context')
        self.apikey = config.get('apikey')
        self.model = ModelFactory.create_model(self,config.get('model','chatgpt'))
        self.model.generate_model(self.apikey)
        self.attachment_file = config.get('attachment_file')

    @abstractmethod
    def response(self) -> list:
        pass


    def get_documents_metadata(self) -> list:
        return []