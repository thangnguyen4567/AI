from flask import Blueprint,request,render_template, Response, stream_with_context
from dotenv import load_dotenv
from services.chatbot import ChatBot
from queue import Queue
from threading import Thread
import asyncio
import markdown

load_dotenv('.env')

chatbot = Blueprint('chatbot', __name__)

def async_to_sync(generator_func):
    def sync_generator(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        gen = generator_func(*args, **kwargs)
        q = Queue()

        def enqueue_data():
            not_done = True
            while not_done:
                try:
                    item = loop.run_until_complete(gen.__anext__())
                    q.put(item)
                except StopAsyncIteration:
                    not_done = False
            q.put(StopIteration)

        thread = Thread(target=enqueue_data)
        thread.start()

        while True:
            item = q.get()
            if item == StopIteration:
                break
            if isinstance(item, list):
                metadata = item[0]
            else:
                yield item

        loop.call_soon_threadsafe(loop.stop)
        thread.join()

    return sync_generator

@chatbot.route('/', methods=['GET'])
def check_api():
    return 'Work'
    
@chatbot.route('/conversations', methods=['POST'])
def get_conversations():
    data = request.get_json()
    chat = ChatBot(data)
    answer = chat.chat_response()
    result = {'answer': markdown.markdown(answer['text']).replace("AI:",""),
              'metadata':chat.get_documents_metadata()}
    return result

@chatbot.route('/conversations_stream', methods=['POST'])
def get_conversations_stream():
    
    data = request.get_json()
    chat = ChatBot(data)
    
    @async_to_sync
    async def generator():
        fullmessage = ''
        async for chunk in chat.chat_response_stream():
            yield chunk

    return Response(generator(), mimetype='text/event-stream', content_type='text/event-stream')

@chatbot.route('/get_metadata', methods=['POST'])
def get_metadata():
    data = request.get_json()
    chat = ChatBot(data)
    result = {'metadata':chat.get_documents_metadata()}
    return result

@chatbot.route('/check_model', methods=['POST'])
def check_model():
    data = request.get_json()
    try:
        chat = ChatBot(data)
        chat.check_chatbot()
        return {'error':False}
    except:
        return {'error':True}

@chatbot.route('/demo', methods=['GET'])
def chatbottemplate():
    return render_template('chatbot.html')