from flask import Blueprint,request,render_template, Response
from dotenv import load_dotenv
import markdown
from tools.helper import async_to_sync,get_chatbot

load_dotenv('.env')

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/conversations', methods=['POST'])
def get_conversations():
    data = request.get_json()
    chat = get_chatbot(data)
    answer = chat.response()
    result = {'answer': markdown.markdown(answer['text']).replace("AI:","")}
    return result

@chatbot.route('/conversations_stream', methods=['POST'])
def get_conversations_stream():
    
    data = request.get_json()
    chat = get_chatbot(data)
    
    @async_to_sync
    async def generator():
        async for chunk in chat.response_stream():
            yield chunk

    return Response(generator(), mimetype='text/event-stream', content_type='text/event-stream')

@chatbot.route('/check_model', methods=['POST'])
def check_model():
    data = request.get_json()
    try:
        chat = get_chatbot(data)
        chat.check_chatbot()
        return {'error':False}
    except:
        return {'error':True}

@chatbot.route('/demo', methods=['GET'])
def chatbottemplate():
    return render_template('chatbot.html')