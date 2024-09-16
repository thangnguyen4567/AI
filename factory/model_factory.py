from model.model_chatgpt import ModelChatGPT
from model.model_gemini import ModelGemini
from model.model_groq import ModelGroq

class ModelFactory:
    def create_model(self,model):
        if model == 'gemini':
            return ModelGemini()
        elif model == 'chatgpt':
            return ModelChatGPT()
        elif model == 'groq':
            return ModelGroq()