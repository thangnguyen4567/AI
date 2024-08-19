from flask import Blueprint,send_file,request
import pyttsx3
from gtts import gTTS
from pydub import AudioSegment

speech = Blueprint('speech', __name__)

@speech.route('/voice', methods=['POST'])
def api_create_speech():
    if 'text' in request.get_json() :
        text = request.get_json()['text']
        tts = gTTS(text=text, lang='vi')
        tts.save("speech.mp3")
        audio = AudioSegment.from_file("speech.mp3")
        faster_audio = audio.speedup(playback_speed=1.3)
        faster_audio.export("speech.mp3", format="mp3")
    return send_file('speech.mp3', mimetype='audio/mpeg')




