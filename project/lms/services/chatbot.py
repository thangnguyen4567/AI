from factory.services.chatbot import ChatbotServices
from project.lms.context.context import ContextLMS

class ChatBot(ChatbotServices):

    def __init__(self,config):
        super().__init__(config)

        if self.context is not None:
            self.context = ContextLMS()
            aggregation_question = self.context.aggregation_question_context(self.chat_history,self.question)
            self.prompt = self.context.retriever_document(self.contextdata,aggregation_question)