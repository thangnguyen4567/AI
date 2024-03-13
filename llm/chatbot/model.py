from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from dotenv import load_dotenv
load_dotenv('.env')
class ChatConverstation():
    def __init__(self) -> None:
        self.llm = GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyCG-B02IPEKbwwzfSzP4gyNX6J46TVpZ0k")
        # self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    def get_conversation_chain(self,message) -> list:
        num_tokens = 0
        for value in message:
            num_tokens += (len(value.content)/4) if hasattr(value,'content') else (len(value.prompt.template) / 4)  # Use 4 as an approximation for the number of characters per token
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        prompt = ChatPromptTemplate(messages=message)
        conversation = LLMChain(
            llm=self.llm,    
            prompt=prompt,
            verbose=True,
            memory=memory,
        )
        print(f"///////////////// Using {num_tokens} tokens (approx) //////////////////")
        return conversation
    
    def get_conversation_message(self) -> list:
        message = [SystemMessagePromptTemplate.from_template(self.prompt)]
        for chat in self.chat_history:
            if 'human' in chat:
                message.append(HumanMessage(content=chat['human']))
            if 'bot' in chat and chat['bot'] != None:
                message.append(AIMessage(content=chat['bot']))
        message.append(HumanMessagePromptTemplate.from_template("{question}"))
        return message