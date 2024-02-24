from flask import Blueprint,request,session
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain_community.vectorstores.redis import RedisNum
from config.config_vectordb import VectorDB
load_dotenv('.env')
chatbot = Blueprint('chatbot', __name__)
@chatbot.route('/', methods=['GET'])
def check_api():
    return 'Work'

@chatbot.route('/api/start', methods=['GET'])
def start_chat():
    if 'chat_history' in session:
        session.pop('chat_history')
    return 'Work'

@chatbot.route('/api/conversations', methods=['POST'])
def create_item():
    if 'chat_history' not in session:
        session['chat_history'] = []
    data = request.get_json()
    conversation = get_converstation_chain(session['chat_history'],data)
    result = conversation(
        {"question": data['question']}
    )
    answer = {'answer':result['text'].replace("AI:","")}
    chat_history = session['chat_history']
    chat_history.append({"human":data['question']})
    chat_history.append({"bot":result['text']})
    session['chat_history'] = chat_history
    return answer

def get_converstation_chain(history,data):
    if "courseid" in data:
        iscourseid = RedisNum("courseid") == int(data['courseid'])
        docs = VectorDB().connect_vectordb('chatbot').similarity_search(data['question'],k=10,filter=iscourseid)
        context = """
            Bạn là AI trợ giảng Elearning Pro , hỗ trợ trả lời ,tóm tắt những thông tin trong khóa học:
            - Chỉ trả lời nhưng thông tin có nội dung dưới đây những thông tin bên ngoài không trả lời
            - Khóa học học có những nội dung như sau:
        """
    else:
        docs = VectorDB().connect_vectordb('chatbot').similarity_search(data['question'],k=10)
        context = """
            Bạn là AI trợ giảng Elearning Pro , hỗ trợ trả lời ,tóm tắt những thông tin trên hệ thống:
        """
    for value in docs:
        context += value.page_content
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyCG-B02IPEKbwwzfSzP4gyNX6J46TVpZ0k")
    message = [SystemMessagePromptTemplate.from_template(context)]
    for chat in history:
        if 'human' in chat:
            message.append(HumanMessage(content=chat['human']))
        if 'bot' in chat:
            message.append(AIMessage(content=chat['bot']))
    message.append(HumanMessagePromptTemplate.from_template("{question}"))
    prompt = ChatPromptTemplate(messages=message)
    conversation = LLMChain(
        llm=llm,    
        prompt=prompt,
        verbose=True,
        memory=memory,
    )
    return conversation
