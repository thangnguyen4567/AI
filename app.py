from routes.chatbot import chatbot  
from routes.report import report
from routes.speech import speech
from flask import Flask,current_app
from flask_cors import CORS
from config.config_sqldb import config_sqldb
from config.config_vectordb import config_vectordb

app = Flask(__name__, template_folder="view")
app.cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
with app.app_context():
    current_app.sql_db = config_sqldb()
    current_app.vector_db = config_vectordb()
app.register_blueprint(chatbot, url_prefix='/chatbot')
app.register_blueprint(report, url_prefix='/report')
app.register_blueprint(speech, url_prefix='/speech')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8009,use_reloader=False)