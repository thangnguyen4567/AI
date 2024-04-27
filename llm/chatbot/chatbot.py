from llm.factory.context_factory import ContextFactory
from llm.factory.model_factory import ModelFactory
class ChatBot():

    def __init__(self,config):

        if "question" in config:
            self.question = config['question']
            
        if "chat_history" in config:
            self.chat_history = config['chat_history']

        if "contextdata" in config:
            self.contextdata = config['contextdata']

        if "context" in config:
            self.context = config['context']

        if "project" in config:
            self.project = config['project']
        else:
            self.project = None

        if "model" in config:
            self.model = config['model']
        else:
            self.model = 'groq'

        self.model = ModelFactory.create_model(self,self.model)
        self.context = ContextFactory.create_context(self,self.context)
        self.prompt = self.context.retriever_document(self.contextdata,self.question)

    def chat_reponse(self) -> list:
        
        self.model.generate_model(self.project)

        message = self.model.get_conversation_message(self.prompt,self.context.chat_history)

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