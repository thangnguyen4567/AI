from factory.services.chatbot import ChatbotServices
from project.lms.context.context import Context
from langchain_community.callbacks.manager import get_openai_callback
import json

class ChatBot(ChatbotServices):

    def __init__(self,config):
        super().__init__(config)

        if self.context is not None:
            self.context = Context()
            if len(self.question) <= 35:
                aggregation_question = self.context.aggregation_question_context(self.chat_history,self.question)
            else:
                aggregation_question = self.question
            self.prompt = self.context.retriever_document(self.contextdata,aggregation_question)

    async def response_stream(self):
        
        message = self.model.get_conversation_message(self.prompt,self.chat_history)
        chain = self.model.get_conversation_chain_stream(message)

        with get_openai_callback() as cb: 
            async for chunk in chain.astream({"question": self.question}):
                data = {
                    "message": chunk
                }
                yield f"{json.dumps(data)}"
            data = {
                "usage": {
                    "prompt_tokens": cb.prompt_tokens, 
                    "completion_tokens": cb.completion_tokens,
                    "total_tokens": cb.total_tokens,
                    "total_cost": cb.total_cost
                }
            }
            yield f"{json.dumps(data)}"
            if 'resource' in self.context.selecttopics:
                yield json.dumps({'topic': 'resource'})
            elif 'course' in self.context.selecttopics:
                yield json.dumps({'topic': 'course'})
            elif any(topic.strip() in ['student', 'teacher', 'manager'] for topic in self.context.selecttopics):
                yield json.dumps({'topic': 'hdsd'})