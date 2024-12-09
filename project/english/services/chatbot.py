from factory.services.chatbot import ChatbotServices
from project.english.context import ContextEnglish

class ChatBot(ChatbotServices):
    
    def __init__(self,config):
        super().__init__(config)
        self.module = config.get('module')

        if self.context is not None:
            self.context = ContextEnglish(self.module)
            aggregation_question = self.context.aggregation_question_context(self.chat_history,self.question)
            self.prompt = self.context.retriever_document(self.contextdata,aggregation_question)

    def response(self) -> list:
    
        message = self.model.get_conversation_message(self.prompt,self.chat_history)
        chain = self.model.get_conversation_chain(message)

        response = chain({"question": self.question}) 

        return response