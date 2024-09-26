from factory.base.services import Services

class Editor(Services):

    def __init__(self,config):

        super().__init__(config)

        self.query = config.get('query')
        self.prompt = config.get('prompt')

    def response(self) -> list:
        
        message = self.model.get_editor_message(self.context,self.query)
        response = self.model.llm.invoke(message)

        return response