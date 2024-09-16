from flask import request,Blueprint
# from llm.services.chatbot import ChatBot
from project.report.init import PowerAI


report = Blueprint('report', __name__)

@report.route('/api/answer_query_v2', methods=['POST'])
def create_query_sql_custom():

    requestJson = request.get_json()
    question = requestJson["question"]
    
    # data = {
    #     'context':'report',
    #     'question': question,
    #     'contextdata': [],
    # }
    # chat = ChatBot(data)
    # query = chat.chat_response()
    # answer = query['text'].replace("\n", " ")
    # result = {'question': question, 'answer': answer}
    # return result
    llm = PowerAI()

    query = llm.generate_sql(question)
    answer = query.replace("\n", " ")
    result = {'question': question, 'answer': answer}

    return result