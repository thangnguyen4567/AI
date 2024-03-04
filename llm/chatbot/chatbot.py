from llm.chatbot.context import Context
from llm.chatbot.model import ChatConverstation


class ChatBot(Context, ChatConverstation):

    def __init__(self):
        Context.__init__(self)
        ChatConverstation.__init__(self)

    def chat_reponse(self, question: str, history: list, contextdata: list, context: str) -> list:
        prompt = self.get_context(context)
        prompt += self.retriever_document(question,contextdata,context)
        message = self.get_conversation_message(prompt,history)
        chain = self.get_conversation_chain(message)
        reponse = chain({"question": question})   
        return reponse
