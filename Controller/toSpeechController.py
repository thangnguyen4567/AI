import pyttsx3, base64, os
from flask import Blueprint,jsonify, render_template,request
import time

def fn_create_speech(text):
    # text = request.data.decode('utf-8')
    timecreate = int(time.time())
    file_name = str(timecreate) + ".mp3"
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    vi_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
    engine.setProperty("voice", vi_voice_id)
    engine.save_to_file(text, file_name)
    engine.runAndWait()
    
    rename = move_file_dicretory(file_name)

    with open(rename, 'rb') as f:
        mp3_bytes = f.read()

    mp3_file = base64.b64encode(mp3_bytes).decode("utf-8")

    return mp3_file



def move_file_dicretory(file_name):
    path = './root/file_speech/'
    rename = path + file_name
    
    if os.path.exists(rename):
        os.remove(rename)
    os.rename(file_name, rename)
    return rename