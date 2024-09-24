from flask import request,Blueprint
from project.lms.services.question import Question


generate = Blueprint('generate', __name__)

@generate.route('/question', methods=['POST'])
def create_question():
    data = request.get_json()
    llm = Question(data)
    result = llm.response()
    return result
