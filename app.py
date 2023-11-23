from routes.chatbot import chatbot  # Import blueprint từ file auth.py
from routes.report import report
from routes.speech import speech
from init import create_app
app = create_app()
# Đăng ký blueprint vào ứng dụng Flask
app.register_blueprint(chatbot, url_prefix='/chatbot')  # Đặt đường dẫn tiền tố '/auth' cho các routes trong blueprint
app.register_blueprint(report, url_prefix='/report')
app.register_blueprint(speech, url_prefix='/speech')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8009, debug=True, use_reloader=False)