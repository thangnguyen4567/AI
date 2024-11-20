from routes.chatbot import chatbot  
from routes.report import report
from routes.speech import speech
from routes.training import training
from routes.generate import generate
from flask import Flask
from flask_cors import CORS
from logging.handlers import RotatingFileHandler
import logging
import os
import ptvsd
from flasgger import Swagger

app = Flask(__name__, template_folder="templates")
swagger = Swagger(app)

# ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True)

app.secret_key = 'secret_key'
app.cors = CORS(app, resources={r"*": {"origins": "*"}},supports_credentials=True)

# Ensure the logs directory exists
logs_dir = os.path.join(app.root_path, 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

handler = RotatingFileHandler(os.path.join(logs_dir, 'error_log.log'), maxBytes=102400, backupCount=10)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

app.register_blueprint(chatbot, url_prefix='/chatbot')
app.register_blueprint(report, url_prefix='/report')
app.register_blueprint(speech, url_prefix='/speech')
app.register_blueprint(training, url_prefix='/training')
app.register_blueprint(generate, url_prefix='/generate')

@app.route('/')
def home():
    return {'text':'Welcome to API'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,use_reloader=True)