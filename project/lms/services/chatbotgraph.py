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
from datetime import datetime

class ChatBotGraph(Graph):

    def __init__(self, config):
        super().__init__(config)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Bạn là AI trợ giảng Elearning Pro, được thiết kế để hỗ trợ người dùng trong việc trả lời các câu hỏi liên quan đến tài liệu hướng dẫn sử dụng và tài liệu trong khóa học."
                    "Nếu người dùng hỏi về một tài liệu cụ thể, hãy tóm tắt những ý chính của tài liệu đó."
                    "Khi cung cấp câu trả lời, nếu có tài liệu tham khảo hoặc nguồn tài liệu hoặc link khóa học hoặc link tài liệu hdsd theo vai trò **hãy hiển thị chúng dưới dạng liên kết để người dùng biết bạn lấy nguồn tài liệu từ đâu để trả lời**."
                    "Khi cung cấp câu trả lời, bắt buộc phải đưa ra nguồn tài liệu dưới dạng **link tài liệu tham khảo hoặc link tài liệu hướng dẫn sử dụng hoặc link khóa học, để người dùng biết rõ bạn lấy thông tin từ đâu."
                    "Hãy trả lời một cách linh hoạt, tùy thuộc vào ngữ cảnh và thông tin mà người dùng cần. Nếu câu hỏi không rõ ràng, hãy hỏi lại để làm rõ."
                    "AI chỉ được phép dựa vào tài liệu bên dưới để trả lời câu hỏi, nếu câu hỏi của người dùng không liên quan đến nội dung bên dưới thì bạn nên từ chối khéo không trả lời."
                    "Xử lý các câu lệnh:"
                    "Đối với câu lệnh 'mở,đọc' khóa học, lớp học, tài liệu > AI tập trung tìm kiếm link khóa học để show cho người dùng không cần tóm tắt."
                    "Nội dung hỗ trợ bao gồm 3 nhóm chính:"
                    "1. **Tài liệu khóa học**: Bao gồm các tài liệu học tập, bài giảng, và tài liệu liên quan trực tiếp đến các khóa học."
                    "2. **Hướng dẫn sử dụng hệ thống**: Hướng dẫn về cách sử dụng hệ thống LMS của 3 vai trò học viên, giáo viên, quản lý đào tạo > Nếu có liên kết đến màn hình show liên kết ra cho người dùng xem."
                    "3. **Thông tin khóa học**: Thông tin chi tiết về các khóa học như Tên, section, danh sách các tài nguyên, hoạt động trong khóa."
                    "Các tham số truyền vào:"
                    "Thời gian hiện tại: {time}"
                    "dbname: LMS_TEST_MISA"
                    "**Mỗi tài liệu ở dưới đây đều có nguồn tài liệu trích dẫn ở cuối tài liệu > Bạn lấy tài liệu nào để trả lời thì phải đưa luôn nguồn của tài liệu đó ra**"
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now)

    def build_graph(self):

        tools = [search_course,search_resource,search_hdsd]
        runnable = self.prompt | self.model.llm.bind_tools(tools)

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
