from project.lms.tools.search_resource import search_resource
from project.lms.tools.search_course import search_course
from project.lms.tools.search_hdsd import search_hdsd
from factory.services.graph import Graph
from langgraph.graph import START
from project.lms.context.context import Context
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from langgraph.graph.message import AnyMessage, add_messages
import uuid
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
import json

class ChatBotGraph(Graph):

    def __init__(self, config):
        super().__init__(config)
        
        if self.context is not None:
            self.context = Context()
            if len(self.question) <= 35:
                aggregation_question = self.context.aggregation_question_context(self.chat_history, self.question)
            else:
                aggregation_question = self.question
            self.prompt = self.context.retriever_document(self.contextdata, aggregation_question, True)

    def build_graph(self):

        tools = [search_course,search_resource]
        message = self.model.get_conversation_message(self.prompt,self.chat_history)
        # Bỏ phần từ cuối cùng của message
        message.pop()
        message.append(MessagesPlaceholder(variable_name="messages"))

        prompt = ChatPromptTemplate.from_messages(message)
        runnable = prompt | self.model.llm.bind_tools(tools,tool_choice="any")

        try:
            self.builder.add_node("assistant", Assistant(runnable))
            self.builder.add_node("tools", self.create_tool_node_with_fallback(tools))
            self.builder.add_edge(START, "assistant")
            self.builder.add_conditional_edges(
                "assistant",
                tools_condition,
            )
            self.builder.add_edge("tools", "assistant")
            self.builder.add_node("end")
            self.builder.add_edge("assistant", "end", condition=lambda state: state["messages"][-1][1].lower() in ["exit", "quit"])
        except Exception as e:
            print(e)

        memory = MemorySaver()

        return self.builder.compile(checkpointer=memory)
    
    async def response_stream(self):
        graph = self.build_graph()
        # try:
        #     img = graph.get_graph(xray=True).draw_mermaid_png()
        #     with open("output.png", "wb") as f:
        #         f.write(img)
        #     print("Image saved as output.png")
        # except Exception as e:
        #     print(f"Error: {e}")

        thread_id = str(uuid.uuid4())
        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }
        # events = graph.invoke(
        #     {"messages": [("user", self.question)]}, config=config
        # )
        # return events["messages"][-1].content
    
        async for event in graph.astream_events({"messages": [("user", self.question)]}, config=config, version="v1"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    data = {
                        "message": content
                    }
                    yield f"{json.dumps(data)}"
    
    def response(self):

        pass

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            state = {**state}
            result = self.runnable.invoke(state)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}
