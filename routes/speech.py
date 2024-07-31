from flask import Blueprint,send_file,request
import pyttsx3
from gtts import gTTS

speech = Blueprint('speech', __name__)

@speech.route('/api/voice', methods=['POST'])
def api_create_speech():
    if 'text' in request.get_json() :
        text = request.get_json()['text']
        tts = gTTS(text=text, lang='vi')
        tts.save("speech.mp3")
    return send_file('speech.mp3', mimetype='audio/mpeg')




