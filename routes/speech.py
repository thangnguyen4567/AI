from flask import Blueprint,send_file,request
from gtts import gTTS
from pydub import AudioSegment
import io

speech = Blueprint('speech', __name__)

@speech.route('/voice', methods=['POST'])
def api_create_speech():
    """
    ---
    tags:
      - Chatbot
    summary: Chuyển văn bản thành giọng nói
    parameters:
      - in: body
        name: body
        required: true
        description: JSON payload containing the conversation data
        schema:
          type: object
          properties:
            text:
              type: string
              description: Chuyển văn bản thành giọng nói
    responses:
      200:
        description: Trả về file âm thanh MP3
        content:
          audio/mpeg:
            schema:
              type: string
              format: binary
      400:
        description: Không có dữ liệu text
        content:
          text/plain:
            schema:
              type: string
              example: 'Không có dữ liệu'
    """
    data = request.get_json()
    text = data.get('text')
    lang = data.get('lang','vi')
    
    tts = gTTS(text=text, lang=lang)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    
    audio_buffer.seek(0)
    audio = AudioSegment.from_file(audio_buffer, format="mp3")
    playback_speed = 1.1 if lang == 'en' else 1.3
    faster_audio = audio.speedup(playback_speed=playback_speed)
    
    output_buffer = io.BytesIO()
    faster_audio.export(output_buffer, format="mp3")
    output_buffer.seek(0)

    return send_file(output_buffer, mimetype='audio/mpeg')
