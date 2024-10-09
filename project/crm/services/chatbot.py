from factory.services.chatbot import ChatbotServices

class ChatBot(ChatbotServices):

    def __init__(self,config):
        super().__init__(config)

        if self.context is not None:
            self.prompt = ''