from factory.services.chatbot import ChatbotServices
from project.lms.context.context import Context
from langchain_community.callbacks.manager import get_openai_callback
import json
from project.lms.tools.search_resource import search_resource
from project.lms.tools.search_course import search_course
from project.lms.tools.search_hdsd import search_hdsd

class ChatBotAgent(ChatbotServices):

    def __init__(self, config):
        super().__init__(config)
        
        if self.context is not None:
            self.context = Context()
            if len(self.question) <= 35:
                aggregation_question = self.context.aggregation_question_context(self.chat_history, self.question)
            else:
                aggregation_question = self.question
            self.prompt = self.context.retriever_document(self.contextdata, aggregation_question, True)

    async def response_stream(self):

        tools = [search_resource, search_course, search_hdsd]
        message = self.model.get_conversation_message(self.prompt,self.chat_history)
        agent = self.model.get_agent(tools,message)

        with get_openai_callback() as cb:   
            async for event in agent.astream_events({"question": self.question},version="v1",):
                kind = event["event"]
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        data = {
                            "message": content
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