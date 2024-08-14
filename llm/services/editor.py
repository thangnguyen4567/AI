from llm.factory.context_factory import ContextFactory
from llm.factory.model_factory import ModelFactory
from langchain_openai import ChatOpenAI

class Editor():

    def __init__(self,config):

        self.system = config.get('system')
        self.query = config.get('query')
        self.context = config.get('context')
        self.apikey = config.get('apikey')
        self.prompt = config.get('prompt')
        self.model = ModelFactory.create_model(self,config.get('model','chatgpt'))

    def response(self) -> list:
        
        self.model.generate_model(self.apikey)
        message = self.model.get_editor_message(self.system,self.context,self.query)
        response = self.model.llm.invoke(message)

        return response