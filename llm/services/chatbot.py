from llm.factory.context_factory import ContextFactory
from llm.factory.model_factory import ModelFactory

class ChatBot():

    def __init__(self,config):

        self.question = config.get('question','test')
        self.chat_history = config.get('chat_history')
        self.contextdata = config.get('contextdata')
        self.context = config.get('context')
        self.project = config.get('project')
        self.apikey = config.get('apikey')
        self.model = ModelFactory.create_model(self,config.get('model','groq'))

        if self.context is not None:
            self.context = ContextFactory.create_context(self,self.context)
            self.prompt = self.context.retriever_document(self.contextdata,self.question)

    def check_chatbot(self):
        
        self.model.generate_model(self.apikey)
        chain = self.model.get_conversation_chain()
        chain({"question": self.question}) 

    def chat_response(self) -> list:
        
        self.model.generate_model(self.apikey)
        message = self.model.get_conversation_message(self.prompt,self.chat_history)
        chain = self.model.get_conversation_chain(message)

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