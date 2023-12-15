from flask import request,jsonify,Blueprint
from controller.reportController import reportController

report = Blueprint('report', __name__)

@report.route('/api/answer_query_v2', methods=['POST'])
def create_query_sql_custom():
    return jsonify(reportController(request))