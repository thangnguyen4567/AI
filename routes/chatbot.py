from flask import Blueprint,request,session
from dotenv import load_dotenv
from llm.chatbot.chatbot import ChatBot
load_dotenv('.env')
chatbot = Blueprint('chatbot', __name__)
chat = ChatBot()

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
    if 'chat_history' not in session:
        session['chat_history'] = []
    data = request.get_json()
    answer = chat.chat_reponse(question=data['question'],history=session['chat_history'],contextdata=data['contextdata'],context=data['context'])
    result = {'answer':answer['text'].replace("AI:","")}
    chat_history = session['chat_history']
    chat_history.append({"human":data['question']})
    chat_history.append({"bot":answer['text']})
    session['chat_history'] = chat_history
    return result
