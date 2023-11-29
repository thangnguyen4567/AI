from flask import request, session,Blueprint
from Controller.answerController import get_conversation_chain

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/', methods=['GET'])
def check_api():
    return 'Work'

@chatbot.route('/api/conversations', methods=['GET'])
def create_item():
    question = request.args.get('question')
    conversation = get_conversation_chain()
    if(session.get('chat_history',None)):
        result = conversation({'question': question,'chat_history': session.get('chat_history',None)})
    else:
        result = conversation({'question': question,'chat_history': []})
    session['chat_history'] = [(question, result["answer"])]
    return result