from flask import Blueprint,request
from dotenv import load_dotenv
from services.editor import Editor
import markdown

load_dotenv('.env')

editor = Blueprint('editor', __name__)

@editor.route('/completions', methods=['POST'])
def get_conversations():
    data = request.get_json()
    editor = Editor(data)
    answer = editor.response()
    if hasattr(answer, 'content'):
        result = {'answer':markdown.markdown(answer.content)}
    else:
        result = {'answer':markdown.markdown(answer)}
    return result