from flask import request,Blueprint
from project.lms.services.course import Course
from project.lms.services.question import Question
from project.lms.services.editor import Editor
from project.lms.services.assignment import Assignment
import markdown

generate = Blueprint('generate', __name__)

@generate.route('/question', methods=['POST'])
def create_question():
    data = request.get_json()
    service = Question(data)
    result = service.response()
    return result

@generate.route('/content', methods=['POST'])
def generate_content():
    data = request.get_json()
    type = data.get('type')

    if type == 'question':
        generate = Question(data)
    elif type == 'course':
        generate = Course(data)
    elif type == 'assignment':
        generate = Assignment(data)
    elif type == 'editor':
        generate = Editor(data)
        
    result = generate.response()

    return result