from controller.toSpeechController import fn_create_speech
from flask import Blueprint,jsonify, render_template,request
speech = Blueprint('speech', __name__)

@speech.route('/api/view_speech', methods=['POST', 'GET'])
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

@speech.route('/api/create_speak', methods=['POST'])
def api_create_speech():
    text = request.data.decode('utf-8')
    return jsonify({'mp3_file': fn_create_speech(text)})