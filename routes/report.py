from flask import request,Blueprint
from llm.services.chatbot import ChatBot

report = Blueprint('report', __name__)

@report.route('/api/answer_query_v2', methods=['POST'])
def create_query_sql_custom():
    question = request.get_json()["question"]
    data = {
        'context':'report',
        'question': question,
        'contextdata': [],
    }
    chat = ChatBot(data)
    query = chat.chat_response()
    answer = query['text'].replace("\n", " ")
    result = {'question': question, 'answer': answer}
    return result