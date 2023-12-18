from routes.chatbot import chatbot  
from routes.report import report
from routes.speech import speech
from routes.training import training
from flask import Flask,current_app
from flask_cors import CORS
from config.config_sqldb import SQLDB
from logging.handlers import RotatingFileHandler
import logging
import os

app = Flask(__name__, template_folder="templates")
app.cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
handler = RotatingFileHandler(os.path.join(app.root_path, 'logs', 'error_log.log'), maxBytes=102400, backupCount=10)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

with app.app_context():
    sql_db = SQLDB()
    current_app.sql_db = sql_db.config_sqldb()
app.register_blueprint(chatbot, url_prefix='/chatbot')
app.register_blueprint(report, url_prefix='/report')
app.register_blueprint(speech, url_prefix='/speech')
app.register_blueprint(training, url_prefix='/training')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8009,use_reloader=True)