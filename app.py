from flask import Flask, request, session

from Model.questionModel import Question
from Controller.answerController import get_conversation_chain
import streamlit as st

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route('/api/conversations', methods=['POST'])
def create_item():
    data = request.get_json()
    conversation = get_conversation_chain()
    if(session.get('chat_history',None)):
        result = conversation({'question': data['question'],'chat_history': session.get('chat_history',None)})
    else:
        result = conversation({'question': data['question'],'chat_history': []})

    session['chat_history'] = [(data['question'], result["answer"])]
    return result

if __name__ == '__main__':
    app.run(debug=True)