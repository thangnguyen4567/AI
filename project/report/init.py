from project.report.vectorstore import VectorStore
from project.report.openai_chat import OpenAI_Chat

class PowerAI(VectorStore, OpenAI_Chat):
    def __init__(self):
        VectorStore.__init__(self)
        OpenAI_Chat.__init__(self)
