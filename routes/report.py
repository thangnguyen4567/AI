from flask import request,Blueprint
from llm.init import PowerAI

llm = PowerAI()
report = Blueprint('report', __name__)

@report.route('/api/answer_query_v2', methods=['POST'])
def create_query_sql_custom():
    requestJson = request.get_json()
    question = requestJson["question"]
    result = llm.generate_sql(question)
    return result