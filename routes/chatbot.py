from flask import Blueprint,request,render_template, Response
from dotenv import load_dotenv
import markdown
from tools.helper import async_to_sync,get_chatbot
from project.lms.services.chatbotgraph import ChatBotGraph

load_dotenv('.env')

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/conversations', methods=['POST'])
def get_conversations():
    """
    ---
    tags:
      - Chatbot
    summary: Get chatbot conversation response
    parameters:
      - in: body
        name: body
        required: true
        description: JSON payload containing the conversation data
        schema:
          type: object
          properties:
            question:
              type: string
              description: The input text for the chatbot
            question:
              type: string
              description: The input text for the chatbot
              default: "Hello, how can I help you?"
            context:
              type: string
              description: The context of the chatbot
              default: "lms"
            chat_history:
              type: array
              items:
                type: object
                properties:
                  human:
                    type: string
                    description: The human message
                  bot:
                    type: string
                    description: The bot message
              description: The chat history of the chatbot
    responses:
      200:
        description: Successful response
        schema:
          type: object
          properties:
            answer:
              type: string
              description: The chatbot's response in html format
    """
    data = request.get_json()
    chat = get_chatbot(data)
    answer = chat.response()
    result = {'answer': markdown.markdown(answer['text']).replace("AI:","")}
    return result

@chatbot.route('/conversations_stream', methods=['POST'])
def get_conversations_stream():
    """
    ---
    tags:
      - Chatbot
    summary: Get chatbot conversation response streaming
    parameters:
      - in: body
        name: body
        required: true
        description: JSON payload containing the conversation data
        schema:
          type: object
          properties:
            question:
              type: string
              description: The input text for the chatbot
            question:
              type: string
              description: The input text for the chatbot
              default: "Hello, how can I help you?"
            context:
              type: string
              description: The context of the chatbot
              default: "lms"
            chat_history:
              type: array
              items:
                type: object
                properties:
                  human:
                    type: string
                    description: The human message
                  bot:
                    type: string
                    description: The bot message
              description: The chat history of the chatbot
    responses:
      200:
        description: Successful response
        content:
          text/event-stream:
            schema:
              type: string
              description: The chatbot's response text
    """
    data = request.get_json()
    chat = get_chatbot(data)
    
    @async_to_sync
    async def generator():
        async for chunk in chat.response_stream():
            yield chunk

    return Response(generator(), mimetype='text/event-stream', content_type='text/event-stream')

@chatbot.route('/agent', methods=['POST'])
def chatbot_agent():
    """
    ---
    tags:
      - Chatbot
    summary: Get chatbot conversation response streaming
    parameters:
      - in: body
        name: body
        required: true
        description: JSON payload containing the conversation data
        schema:
          type: object
          properties:
            question:
              type: string
              description: The input text for the chatbot
            question:
              type: string
              description: The input text for the chatbot
              default: "Hello, how can I help you?"
            context:
              type: string
              description: The context of the chatbot
              default: "lms"
            chat_history:
              type: array
              items:
                type: object
                properties:
                  human:
                    type: string
                    description: The human message
                  bot:
                    type: string
                    description: The bot message
              description: The chat history of the chatbot
    responses:
      200:
        description: Successful response
        content:
          text/event-stream:
            schema:
              type: string
              description: The chatbot's response text
    """
    data = request.get_json()
    chat = get_chatbot(data)
    
    @async_to_sync
    async def generator():
        async for chunk in chat.agent_response():
            yield chunk

    return Response(generator(), mimetype='text/event-stream', content_type='text/event-stream')

@chatbot.route('/demo', methods=['GET'])
def chatbot_demo():
    return render_template('chatbot.html')

@chatbot.route('/graph', methods=['POST'])
def chatbot_graph():
    """
    ---
    tags:
      - Chatbot
    summary: Get chatbot conversation response streaming
    parameters:
      - in: body
        name: body
        required: true
        description: JSON payload containing the conversation data
        schema:
          type: object
          properties:
            question:
              type: string
              description: The input text for the chatbot
            question:
              type: string
              description: The input text for the chatbot
              default: "Hello, how can I help you?"
            context:
              type: string
              description: The context of the chatbot
              default: "lms"
            chat_history:
              type: array
              items:
                type: object
                properties:
                  human:
                    type: string
                    description: The human message
                  bot:
                    type: string
                    description: The bot message
              description: The chat history of the chatbot
    responses:
      200:
        description: Successful response
        content:
          text/event-stream:
            schema:
              type: string
              description: The chatbot's response text
    """
    data = request.get_json()
    try:
        chat = ChatBotGraph(data)
    except Exception as e:
        print(e)
    
    @async_to_sync
    async def generator():
        async for chunk in chat.response_stream():
            yield chunk

    return Response(generator(), mimetype='text/event-stream', content_type='text/event-stream')
