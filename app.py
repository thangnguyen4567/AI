from flask import Flask, request, session
from Controller.answerController import get_conversation_chain
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = 'your_secret_key' 

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

if __name__ == '__main__':
    app.run(host="localhost", port=8181, debug=True)