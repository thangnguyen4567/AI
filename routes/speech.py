from controller.toSpeechController import fn_create_speech
from flask import Blueprint,jsonify, render_template,request
speech = Blueprint('speech', __name__)



@speech.route('/api/view_speech', methods=['GET','POST'])
def speech_view():
    if request.method == 'POST':
        text = request.form['input']
        strBase64 = fn_create_speech(text)
        return render_template("text_speech.html", url_base64 = strBase64)
    else:
        return render_template("text_speech.html", url_base64 = '')


@speech.route('/api/create_speak', methods=['POST'])
def api_create_speech():
    text = request.data.decode('utf-8')
    return jsonify({'mp3_file': fn_create_speech(text)})