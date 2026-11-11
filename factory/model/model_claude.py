from factory.base.model import Model
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.tools import format_to_tool_messages
from langchain.agents.output_parsers.tools import ToolsAgentOutputParser
import os


class ModelClaude(Model):
    def __init__(self):
        Model.__init__(self)

    def generate_model(self, apikey: str):

        # Client có thể gửi `apikey` của provider khác (vd. OpenAI) trong request;
        # chỉ dùng nếu đúng dạng key Anthropic, nếu không lấy từ môi trường.
        if not apikey or not str(apikey).startswith("sk-ant-"):
            apikey = os.getenv("ANTHROPIC_API_KEY")

        # Không truyền temperature/top_p/top_k: Claude Opus 5.5 / Sonnet 5.5
        # từ chối các tham số sampling này (HTTP 400).
        model_name = os.getenv("CLAUDE_MODEL", "claude-haiku-5-5")

        # Các model mới bật adaptive thinking mặc định, stream về content dạng list
        # lẫn block thinking; langchain-core 0.3.x merge chunk lỗi
        # "TypeError: string indices must be integers". Chatbot hỏi đáp không cần
        # thinking nên tắt đi (cũng nhanh và rẻ hơn).
        extra = {}
        if "haiku" in model_name:
            extra["thinking"] = {"type": "disabled"}
        elif "sonnet-5-5" in model_name:
            extra["thinking"] = {"type": "between_tools"}  # Sonnet 5.5 không cho disabled
        # Opus 5.5 không tắt được thinking; nếu gặp lỗi trên hãy dùng haiku/sonnet.

        self.llm = ChatAnthropic(
            model=model_name,
            api_key=apikey,
            max_tokens=4096,
            stream_usage=True,
            **extra,
        )

    def get_agent(self, tools: list, message: list) -> AgentExecutor:
        # Claude trả tool call ở `message.tool_calls`, không phải
        # `additional_kwargs["tool_calls"]` như OpenAI nên cần parser riêng.
        llm_with_tools = self.llm.bind_tools(tools)
        message.append(HumanMessagePromptTemplate.from_template("{question}"))
        message.append(MessagesPlaceholder(variable_name="agent_scratchpad"))
        prompt = ChatPromptTemplate.from_messages(message)

        agent = (
            {
                "question": lambda x: x["question"],
                "agent_scratchpad": lambda x: format_to_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | ToolsAgentOutputParser()
        )

        return AgentExecutor(agent=agent, tools=tools, verbose=True)
