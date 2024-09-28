from factory.base.services import Services

class ChatbotServices(Services):

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