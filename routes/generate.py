from flask import request, Blueprint
from project.lms.services.course import Course
from project.lms.services.question import Question
from project.lms.services.editor import Editor
from project.lms.services.assignment import Assignment
from project.lms.services.feedback import Feedback
from project.lms.services.goal import Goal
from project.hrm.services.goal import Goal as GoalHRM
from project.hrm.services.formula import Formula as FormulaHRM

generate = Blueprint("generate", __name__)


@generate.route("/question", methods=["POST"])
def create_question():
    data = request.get_json()
    service = Question(data)
    result = service.response()
    return result


@generate.route("/content", methods=["POST"])
def generate_content():
    data = request.get_json()
    type = data.get("type")

    if type == "question":
        generate = Question(data)
    elif type == "course":
        generate = Course(data)
    elif type == "assignment":
        generate = Assignment(data)
    elif type == "editor":
        generate = Editor(data)
    elif type == "feedback":
        generate = Feedback(data)
    elif type == "goal":
        generate = Goal(data)
    else:
        return {"error": "Type not found"}

    result = generate.response()

    return result


@generate.route("/content_hrm", methods=["POST"])
def generate_content_hrm():
    data = request.get_json()
    type = data.get("type")

    if type == "goal":
        generate = GoalHRM(data)
    elif type == "formula":
        generate = FormulaHRM(data)
    else:
        return {"error": "Type not found"}

    result = generate.response()

    return result
