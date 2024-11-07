from factory.base.services import Services
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.callbacks.manager import get_openai_callback

class Editor(Services):

    def __init__(self,config):

        super().__init__(config)

        self.query = config.get('query')

    def response(self) -> list:
        
        message = []

        message.append(SystemMessage(content='Answer the question based on the context below'))
        message.append("The response should preserve any HTML formatting, links, and styles in the context.")
        message.append(SystemMessage(content='Context:'+self.query))
        message.append(HumanMessage(content=self.question))

        with get_openai_callback() as cb:
            response = self.model.llm.invoke(message)

        result = {}
        result['response'] = response.content
        result['info'] = {
            'total_tokens': cb.total_tokens,
            'total_cost': cb.total_cost,
            'total_prompt_tokens': cb.prompt_tokens,
            'total_completion_tokens': cb.completion_tokens
        }

        return result