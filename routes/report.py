from flask import request,jsonify,Blueprint
from Controller.reportController import get_conversation_query_sql
from Controller.reportControllerV2 import reportControllerV2

report = Blueprint('report', __name__)

@report.route('/api/answer_query', methods=['POST'])
def create_query_sql():
    return jsonify(get_conversation_query_sql(request))


@report.route('/api/answer_query_v2', methods=['POST'])
def create_query_sql_custom():
    return jsonify(reportControllerV2(request))