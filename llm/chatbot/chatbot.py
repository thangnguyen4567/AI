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

        self.get_context()

        self.retriever_document()

        message = self.get_conversation_message()

        chain = self.get_conversation_chain(message)

        reponse = chain({"question": self.question}) 

        return reponse

    def get_documents_metadata(self) -> list:
        self.retriever_document()
        sources = []
        for document in self.documents:
            dict = {}
            for metadata in self.index_schema['text']:
                dict[metadata['name']] = document.metadata[metadata['name']]
            sources.append(dict)
        return sources