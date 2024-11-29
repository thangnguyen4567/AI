from project.lms.tools.search_student_course import search_student_course
from project.lms.tools.search_teacher_info import search_teacher_info
from factory.services.graph import Graph
from langgraph.prebuilt import ToolNode
from project.lms.context.context import Context
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
import uuid
from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain_core.messages import HumanMessage, AIMessage
import json
from datetime import datetime

class ChatBotGraph(Graph):

    def __init__(self, config):
        super().__init__(config)
        self.userid = config.get('userid')
        self.endpoint = config.get('endpoint')
        if self.context is not None:
            self.context = Context()
            if len(self.question) <= 35:
                self.aggregation_question = self.context.aggregation_question_context(self.chat_history,self.question)
            else:
                self.aggregation_question = self.question

    def build_graph(self):

        self.builder = StateGraph(MessagesState)
        tools = [search_student_course,search_teacher_info]
        try:
            self.builder.add_node("tool_assistant", Assistant(self.model.llm,tools,self.chat_history))
            self.builder.add_node("tools", ToolNode(tools))
            self.builder.add_conditional_edges(
                START,
                self.route_tool,
            )
            self.builder.add_conditional_edges(
                "tool_assistant",
                tools_condition,
            )
            self.builder.add_edge("tools", 'tool_assistant')

        except Exception as e:
            print(e)

        memory = MemorySaver()

        return self.builder.compile(checkpointer=memory)
    
    async def response_stream(self):
        graph = self.build_graph()
        try:
            img = graph.get_graph(xray=True).draw_mermaid_png()
            with open("output.png", "wb") as f:
                f.write(img)
            print("Image saved as output.png")
        except Exception as e:
            print(f"Error: {e}")

        config = {
            "configurable": {
                "thread_id": str(uuid.uuid4()), 
                "checkpoint_id": "1ef663ba-28fe-6528-8002-5a559208592c",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3MzI3ODgxMDEsImp0aSI6ImM0MTFhZDhjLWFkNmYtMTFlZi1iMmViLTAyNDJhYzE0MDAwMyIsImlzcyI6IjEwLjEwLjEwLjE0IiwibmJmIjoxNzMyNzg4MTAxLCJleHAiOjE3MzMzOTI5MDEsInVzZXJpZCI6IjIifQ.Bzm6YcczcqIdFdUxpNHY93T9cTShLz3_EitVC4_NwTR-tA7ALRvuDKKuJeVHdUfsAXx-DPAKRX6Dxofr7w2OJg",
                "endpoint": self.endpoint,
                "userid": self.userid,
                "dbname": self.contextdata['collection']
            }
        }
        async for event in graph.astream_events({"messages": ("user", self.question)}, config=config, version="v1"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    data = {
                        "message": content
                    }
                    yield f"{json.dumps(data)}"
            elif kind == "on_tool_start":
                tool_name = event['name']
                yield f"{json.dumps({'tool': tool_name})}"
    
    def response(self):
        pass

    def route_tool(self, state: MessagesState):
        self.context.selecttopics = self.context.classify_topic(self.aggregation_question, self.context.topics)
        if any(topic.strip() == 'searchdata' for topic in self.context.selecttopics):
            return 'tool_assistant'
        else:
            self.prompt = self.context.retriever_document(self.contextdata,self.question)
            message = self.model.get_conversation_message(self.prompt,self.chat_history)
            chain = self.model.get_conversation_chain(message)
            chain({"question": self.question})
            return END
    
class Assistant:
    def __init__(self, llm, tools, chat_history):
        message = []
        if chat_history is not None:
            for chat in chat_history:
                if 'human' in chat:
                    message.append(HumanMessage(content=chat['human']))
                if 'bot' in chat and chat['bot'] != None:
                    message.append(AIMessage(content=chat['bot']))
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Bạn là một trợ lý AI hỗ trợ quản lý thông tin đào tạo cho cả học viên và giảng viên. "
                    "Nhiệm vụ của bạn là giúp người dùng tra cứu thông tin về lịch học, khóa học, điểm danh, "
                    "và các thông tin liên quan khác"
                    "\nThời gian hiện tại: {time}.",
                ),
                *message,
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now().strftime("%d/%m/%y"))
        self.runnable = self.prompt | llm.bind_tools(tools)

    def __call__(self, state: MessagesState, config: RunnableConfig):
        state = {**state}
        response = self.runnable.invoke(state)
        return {"messages": [response]}