from flask import Flask, request, session, jsonify
from Controller.answerController import get_conversation_chain
from Controller.answerQuerySQL import get_conversation_query_sql

import pyttsx3
from init import create_app

app = Flask(__name__)
engine = pyttsx3.init()

app = create_app()

@app.route('/', methods=['GET'])
def check_api():
    return 'hello world'

@app.route('/api/conversations', methods=['GET'])
def create_item():
    question = request.args.get('question')
    conversation = get_conversation_chain()
    if(session.get('chat_history',None)):
        result = conversation({'question': question,'chat_history': session.get('chat_history',None)})
    else:
        result = conversation({'question': question,'chat_history': []})
    session['chat_history'] = [(question, result["answer"])]
    return result

@app.route('/api/text_to_speech', methods=['GET'])
def text_to_speech():
    text = "Hello world, convert text to speech"
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return text

@app.route('/api/answer_query', methods=['POST'])
def create_query_sql():
    requestJson = request.get_json()
    
    question = requestJson["question"]
    connect_sql = app.config_class
    check_connect = app.config['CONNECT_DB']
    answerQuery = get_conversation_query_sql(requestJson, connect_sql, check_connect)
    answer = answerQuery.replace("\n", " ")
    result = {'question': question, 'answer': answer}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)