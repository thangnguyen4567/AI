from llm.factory.model.model import Model
from langchain_openai import ChatOpenAI
import os

class ModelChatGPT(Model):
    def __init__(self):
        Model.__init__(self)

    def generate_model(self,project: str):

        if project is not None:
            api_key = os.getenv("OPENAI_API_KEY_"+project.upper())
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125",api_key=api_key)
