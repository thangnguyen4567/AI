from flask import Blueprint,request,session
from dotenv import load_dotenv
from llm.chatbot.chatbot import ChatBot
load_dotenv('.env')
chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/', methods=['GET'])
def check_api():
    return 'Work'

@chatbot.route('/api/conversations', methods=['POST'])
def get_conversations():
    data = request.get_json()
    chat = ChatBot(data)
    answer = chat.chat_reponse()
    result = {'answer':answer['text'].replace("AI:",""),
              'metadata':chat.get_documents_metadata()}
    return result

@chatbot.route('/api/get_metadata', methods=['POST'])
def get_metadata():
    data = request.get_json()
    chat = ChatBot(data)
    result = {'metadata':chat.get_documents_metadata()}
    return result
