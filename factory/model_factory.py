from factory.model.model_chatgpt import ModelChatGPT
from factory.model.model_gemini import ModelGemini
from factory.model.model_groq import ModelGroq
from factory.model.model_claude import ModelClaude

class ModelFactory:
    def create_model(self,model):
        if model == 'gemini':
            return ModelGemini()
        elif model == 'chatgpt':
            return ModelChatGPT()
        elif model == 'groq':
            return ModelGroq()
        elif model in ('claude', 'anthropic'):
            return ModelClaude()