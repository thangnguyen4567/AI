from flask import request,session,Blueprint
from controller.answerController import get_conversation_chain
from langchain.prompts import PromptTemplate

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/', methods=['GET'])
def check_api():
    return 'Work'

@chatbot.route('/api/conversations', methods=['GET'])
def create_item():
    prompt_template = PromptTemplate.from_template(
        "Bạn là 1 trợ lý chatbot giúp tôi trả lời những câu hỏi liên quan đến cấu trúc bảng của database mà tôi cung cấp ở trên. {question}"
    )
    if(request.args.get('question')):
        question = request.args.get('question')
    else:
        question = request.get_json()['question']
    conversation = get_conversation_chain()
    if(session.get('chat_history',None)):
        result = conversation({'question': prompt_template.format(question=question),'chat_history': session.get('chat_history',None)})
    else:
        result = conversation({'question': prompt_template.format(question=question),'chat_history': []})
    session['chat_history'] = [(question, result["answer"])]
    return result