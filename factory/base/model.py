from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
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
            message.append(HumanMessagePromptTemplate.from_template("{question}"))

        return message 

    def get_editor_message(self,systems: list,context: str,query: str) -> list:

        message = []

        message.append(SystemMessage(content='Answer the question based on the context below'))
        message.append("The response should be in markdown format.")
        message.append("The response should preserve any HTML formatting, links, and styles in the context.")
        message.append(SystemMessage(content='Cotext:'+context))
        message.append(HumanMessage(content=query))
        
        return message