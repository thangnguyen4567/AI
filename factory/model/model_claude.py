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
        self.llm = ChatAnthropic(
            model=os.getenv("CLAUDE_MODEL", "claude-haiku-5-5"),
            api_key=apikey,
            max_tokens=4096,
            stream_usage=True,
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
