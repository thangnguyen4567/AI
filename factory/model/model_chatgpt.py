from factory.base.model import Model
from langchain_openai import ChatOpenAI
import os

class ModelChatGPT(Model):
    def __init__(self):
        Model.__init__(self)

    def generate_model(self,apikey: str):

        if apikey is None:
            apikey = os.getenv("OPENAI_API_KEY")
            
        self.llm = ChatOpenAI(model="gpt-4o-mini",api_key=apikey,temperature=0.5)
