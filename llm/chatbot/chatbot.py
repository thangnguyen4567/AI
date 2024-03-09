from llm.chatbot.context import Context
from llm.chatbot.model import ChatConverstation


class ChatBot(Context, ChatConverstation):

    def __init__(self,config):
        Context.__init__(self)
        ChatConverstation.__init__(self)
        if "question" in config:
            self.question = config['question']
        if "chat_history" in config:
            self.chat_history = config['chat_history']
        if "contextdata" in config:
            self.contextdata = config['contextdata']
        if "context" in config:
            self.context = config['context']

    def chat_reponse(self) -> list:

        prompt = self.get_context()

        prompt += self.retriever_document()

        message = self.get_conversation_message(prompt)

        chain = self.get_conversation_chain(message)

        reponse = chain({"question": self.question}) 

        return reponse

    def get_documents_metadata(self) -> list:
        metadatas = ['source','title']
        sources = []
        for document in self.documents:
            dict = {}
            for metadata in metadatas:
                dict[metadata] = document.metadata[metadata]
            sources.append(dict)
        return sources