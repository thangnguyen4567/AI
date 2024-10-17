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

    result = generate.response()

    return result

@generate.route('/course', methods=['POST'])
def create_course():
    data = request.get_json()
    service = Course(data)
    result = service.response()
    return result

@generate.route('/editor', methods=['POST'])
def create_editor():
    data = request.get_json()
    editor = Editor(data)
    answer = editor.response()
    if hasattr(answer, 'content'):
        result = {'answer':markdown.markdown(answer.content)}
    else:
        result = {'answer':markdown.markdown(answer)}
    return result

@generate.route('/assignment', methods=['POST'])
def create_assignment():
    data = request.get_json()
    assignment = Assignment(data)
    result = assignment.response()
    return result