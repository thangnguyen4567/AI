from llm.factory.model.model import Model
from langchain_google_genai import GoogleGenerativeAI
import os

class ModelGemini(Model):
    def __init__(self):
        Model.__init__(self)
    
    def generate_model(self,project: str):

        if project is not None:
            api_key = os.getenv("GOOGLE_API_KEY_"+project.upper())
        else:
            api_key = os.getenv("GOOGLE_API_KEY")

        self.llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
