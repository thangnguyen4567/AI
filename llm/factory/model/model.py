from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
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

    def get_conversation_chain(self, message: list) -> list:

        if message == []:
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
    
    def get_conversation_message(self,context: str,chat_history: list) -> list:
        message = [SystemMessagePromptTemplate.from_template(context)]
        for chat in chat_history:
            if 'human' in chat:
                message.append(HumanMessage(content=chat['human']))
            if 'bot' in chat and chat['bot'] != None:
                message.append(AIMessage(content=chat['bot']))
        message.append(HumanMessagePromptTemplate.from_template("{question}"))
        return message