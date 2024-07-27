from llm.factory.model.model_chatgpt import ModelChatGPT
from llm.factory.model.model_gemini import ModelGemini
from llm.factory.model.model_groq import ModelGroq

class ModelFactory:
    def create_model(self,model):
        if model == 'gemini':
            return ModelGemini()
        elif model == 'chatgpt':
            return ModelChatGPT()
        elif model == 'groq':
            return ModelGroq()