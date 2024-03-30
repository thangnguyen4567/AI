from flask import Blueprint,send_file,request
import pyttsx3

speech = Blueprint('speech', __name__)

@speech.route('/api/voice', methods=['POST'])
def api_create_speech():
    if 'text' in request.get_json() :
        text = request.get_json()['text']
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)
        engine.save_to_file(text, 'speech.mp3')
        engine.runAndWait()
    return send_file('speech.mp3', mimetype='audio/mpeg')
