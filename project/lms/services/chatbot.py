from factory.context_factory import ContextFactory
from factory.base.services import Services

class ChatBot(Services):

    def __init__(self,config):
        super().__init__(config)

        if self.context is not None:
            self.context = ContextFactory.create_context(self,self.context)
            aggregation_question = self.context.aggregation_question_context(self.chat_history,self.question)
            self.prompt = self.context.retriever_document(self.contextdata,aggregation_question)

    def check_chatbot(self):
    
        chain = self.model.get_conversation_chain()
        chain({"question": self.question}) 

    def response(self) -> list:
    
        message = self.model.get_conversation_message(self.prompt,self.chat_history)
        chain = self.model.get_conversation_chain(message)

        response = chain({"question": self.question}) 

        return response

    async def response_stream(self):
        
        message = self.model.get_conversation_message(self.prompt,self.chat_history)
        chain = self.model.get_conversation_chain_stream(message)

        async for chunk in chain.astream({"question": self.question}):
            yield chunk