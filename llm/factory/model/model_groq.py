from llm.factory.model.model import Model
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os

class ModelGroq(Model):
    def __init__(self):
        Model.__init__(self)

    def generate_model(self,project: str):

        if project is not None:
            api_key = os.getenv("GROQ_API_KEY_"+project.upper())
        else:
            api_key = os.getenv("GROQ_API_KEY")
            
        self.llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=api_key)
