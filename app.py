from routes.chatbot import chatbot  
from routes.report import report
from routes.speech import speech
from routes.training import training
from flask import Flask
from flask_cors import CORS
from logging.handlers import RotatingFileHandler
import logging
import os
import ptvsd

app = Flask(__name__, template_folder="templates")

ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True)

app.secret_key = 'secret_key'
app.cors = CORS(app, resources={r"*": {"origins": "*"}},supports_credentials=True)
handler = RotatingFileHandler(os.path.join(app.root_path, 'logs', 'error_log.log'), maxBytes=102400, backupCount=10)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

app.register_blueprint(chatbot, url_prefix='/chatbot')
app.register_blueprint(report, url_prefix='/report')
app.register_blueprint(speech, url_prefix='/speech')
app.register_blueprint(training, url_prefix='/training')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8009,use_reloader=True)