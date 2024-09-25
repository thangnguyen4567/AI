from flask import Blueprint,send_file,request
from gtts import gTTS
from pydub import AudioSegment
import io

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

@speech.route('/voice_custom', methods=['POST'])
def api_create_speech_custom():
    if 'text' in request.get_json() :
        text = request.get_json()['text']
        
        tts = gTTS(text=text, lang='vi')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        
        audio_buffer.seek(0)
        audio = AudioSegment.from_file(audio_buffer, format="mp3")
        faster_audio = audio.speedup(playback_speed=1.3)
        
        output_buffer = io.BytesIO()
        faster_audio.export(output_buffer, format="mp3")
        output_buffer.seek(0)

        return send_file(output_buffer, mimetype='audio/mpeg')
    else:
        return 'Không có dữ liệu'
