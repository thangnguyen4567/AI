from flask import Flask, request, session, jsonify, render_template, Response
from Controller.answerController import get_conversation_chain
from Controller.answerQuerySQL import get_conversation_query_sql

from init import create_app, connect_sqldb
from Controller.toSpeechController import fn_create_speech
from config import ConfigDB

app = create_app()

with app.app_context():
    app.config.from_object(ConfigDB)
    connectDB = app.config['CONNECT_DB']
    if connectDB == False:       
        connect_sqldb(app)

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

@app.route('/api/answer_query', methods=['POST'])
def create_query_sql():
    
    return jsonify(get_conversation_query_sql(app, request))

@app.route('/api/view_speech', methods=['POST', 'GET'])
def speech_view():
    if request.method == 'POST':
        text = request.form['speech']
        
        strBase64 = fn_create_speech(text)      
        
        audio = request.form['audio']
        audio.src = 'data:audio/mp3;base64,' + strBase64
        audio.play()

        return render_template('template/text_speech.html')
    else:
        return render_template('template/text_speech.html')

@app.route('/api/create_speak', methods=['POST'])
def api_create_speech():

    text = request.data.decode('utf-8')
    return jsonify({'mp3_file': fn_create_speech(text)})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8009, debug=True)