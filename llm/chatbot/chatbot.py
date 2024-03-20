from llm.chatbot.model import ChatConverstation
from llm.factory.context_factory import ContextFactory

class ChatBot(ChatConverstation):

    def __init__(self,config):
        ChatConverstation.__init__(self)
        if "question" in config:
            self.question = config['question']
        if "chat_history" in config:
            self.chat_history = config['chat_history']
        if "contextdata" in config:
            self.contextdata = config['contextdata']
        if "context" in config:
            self.context = config['context']

        self.context = ContextFactory.create_context(self,self.context)
        self.prompt = self.context.retriever_document(self.contextdata,self.question)

    def chat_reponse(self) -> list:

        message = self.get_conversation_message()

        chain = self.get_conversation_chain(message)

        reponse = chain({"question": self.question}) 

        return reponse

    def get_documents_metadata(self) -> list:
        sources = []
        for document in self.context.documents:
            dict = {}
            for metadata in self.context.index_schema['text']:
                if metadata['name'] in document.metadata:
                    dict[metadata['name']] = document.metadata[metadata['name']]
                    sources.append(dict)
        return sources