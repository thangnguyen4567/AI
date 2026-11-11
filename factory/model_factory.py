from factory.model.model_chatgpt import ModelChatGPT
from factory.model.model_gemini import ModelGemini
from factory.model.model_groq import ModelGroq
from factory.model.model_claude import ModelClaude

class ModelFactory:
    @staticmethod
    def create_model(*args):
        # Chấp nhận cả create_model(model) và create_model(self, model)
        # (code cũ gọi trên class kèm self).
        model = args[-1]
        if model == 'gemini':
            return ModelGemini()
        elif model == 'chatgpt':
            return ModelChatGPT()
        elif model == 'groq':
            return ModelGroq()
        elif model in ('claude', 'anthropic'):
            return ModelClaude()