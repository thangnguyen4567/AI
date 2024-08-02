from flask import Blueprint,request,session
from dotenv import load_dotenv
from llm.services.chatbot import ChatBot

load_dotenv('.env')

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/', methods=['GET'])
def check_api():
    return 'Work'

@chatbot.route('/conversations', methods=['POST'])
def get_conversations():
    data = request.get_json()
    chat = ChatBot(data)
    answer = chat.chat_response()
    result = {'answer':answer['text'].replace("AI:",""),
              'metadata':chat.get_documents_metadata()}
    return result

@chatbot.route('/get_metadata', methods=['POST'])
def get_metadata():
    data = request.get_json()
    chat = ChatBot(data)
    result = {'metadata':chat.get_documents_metadata()}
    return result

@chatbot.route('/check_model', methods=['POST'])
def check_model():
    data = request.get_json()
    try:
        chat = ChatBot(data)
        chat.check_chatbot()
        return {'error':False}
    except:
        return {'error':True}