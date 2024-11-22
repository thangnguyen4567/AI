from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from abc import ABC, abstractmethod 

class Model(ABC):
    def __init__(self) -> None:
        self.llm = ''
    
    @abstractmethod
    def generate_model(self, apikey: str, **kwargs) -> None:
        pass
    
    ##Tạo chain để xử lý câu hỏi
    def get_conversation_chain(self, message: list = None) -> list:

        if message is None:
            message = [SystemMessagePromptTemplate.from_template('')]

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        prompt = ChatPromptTemplate(messages=message)
        conversation = LLMChain(
            llm=self.llm,    
            prompt=prompt,
            verbose=True,
            memory=memory,
        )
        return conversation
    
    ##Tạo chain để xử lý câu hỏi với streaming
    def get_conversation_chain_stream(self, message: list = None) -> list:

        if message is None:
            message = [SystemMessagePromptTemplate.from_template('')]

        parser = StrOutputParser()
        prompt = ChatPromptTemplate(messages=message)
        chain = prompt | self.llm | parser

        return chain

    ##Khởi tạo lịch sử chat
    def get_conversation_message(self,context: str,chat_history: list = None) -> list:

        message = [SystemMessagePromptTemplate.from_template(context)]

        if chat_history is not None:
            for chat in chat_history:
                if 'human' in chat:
                    message.append(HumanMessage(content=chat['human']))
                if 'bot' in chat and chat['bot'] != None:
                    message.append(AIMessage(content=chat['bot']))
            message.append(HumanMessagePromptTemplate.from_template("{messages}"))

        return message 
    
    def get_agent(self,tools: list,message: list) -> AgentExecutor:

        llm_with_tools = self.llm.bind_tools(tools)
        message.append(HumanMessagePromptTemplate.from_template("{question}"))
        message.append(MessagesPlaceholder(variable_name="agent_scratchpad"))
        prompt = ChatPromptTemplate.from_messages(message)
        
        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         message,
        #         ("user", "{question}"),
        #         MessagesPlaceholder(variable_name="agent_scratchpad"),
        #     ]
        # )
        agent = (
            {
                "question": lambda x: x["question"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        return agent_executor