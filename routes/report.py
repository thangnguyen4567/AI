from flask import request,jsonify,Blueprint
from Controller.answerQuerySQL import get_conversation_query_sql

report = Blueprint('report', __name__)

@report.route('/api/answer_query', methods=['POST'])
def create_query_sql():
    return jsonify(get_conversation_query_sql(request))
