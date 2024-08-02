from flask import Blueprint,request,session
from dotenv import load_dotenv
from llm.services.editor import Editor

load_dotenv('.env')

editor = Blueprint('editor', __name__)

@editor.route('/completions', methods=['POST'])
def get_conversations():
    data = request.get_json()
    editor = Editor(data)
    answer = editor.response()
    if hasattr(answer, 'content'):
        result = {'answer':answer.content}
    else:
        result = {'answer':answer}
    return result