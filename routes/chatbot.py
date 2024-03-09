from flask import Blueprint,request,session
from dotenv import load_dotenv
from llm.chatbot.chatbot import ChatBot
load_dotenv('.env')
chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/', methods=['GET'])
def check_api():
    session['test'] = 'abcd'
    return 'Work'

@chatbot.route('/api/start', methods=['GET'])
def start_chat():
    if 'chat_history' in session:
        session.pop('chat_history')
    return 'Work'

@chatbot.route('/api/conversations', methods=['POST'])
def create_item():
    data = request.get_json()
    chat = ChatBot(data)
    answer = chat.chat_reponse()
    result = {'answer':answer['text'].replace("AI:",""),
              'metadata':chat.get_documents_metadata()}
    return result

@chatbot.route('/api/get_metadata', methods=['POST'])
def create_item():
    data = request.get_json()
    chat = ChatBot(data)
    result = {'metadata':chat.get_documents_metadata()}
    return result
