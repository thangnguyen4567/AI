from factory.base.training import Training
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema import Document
from pathlib import Path
import os

class TrainingChatbot(Training):
    def __init__(self):
        super().__init__()

        self.columns = ['content','url','image','type','category']
        self.context = "highlands"

    def save_training_data(self,data):
        pass

    def check_training_duplication(self):
        pass
    
