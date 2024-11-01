from factory.base.model import Model
from langchain_google_genai import GoogleGenerativeAI
import os

class ModelGemini(Model):
    def __init__(self):
        Model.__init__(self)
    
    def generate_model(self,apikey: str):

        if apikey is None or apikey == '':
            apikey = os.getenv("GOOGLE_API_KEY")

        self.llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=apikey)
