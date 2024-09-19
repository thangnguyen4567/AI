from flask import request,Blueprint
from project.lms.services.createquestion import CreateQuestion


generate = Blueprint('generate', __name__)

@generate.route('/question', methods=['POST'])
def create_question():
    data = request.get_json()
    llm = CreateQuestion(data)
    result = llm.response()
    return result
