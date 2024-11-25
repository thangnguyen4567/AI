from flask import Blueprint,request,render_template, Response
from dotenv import load_dotenv
import markdown
from tools.helper import async_to_sync,get_chatbot
from project.lms.services.chatbotgraph import ChatBotGraph
from project.lms.services.chatbotagent import ChatBotAgent
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
    chat = ChatBotAgent(data)
    
    @async_to_sync
    async def generator():
        async for chunk in chat.response_stream():
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
    chat = ChatBotGraph(data)
    
    @async_to_sync
    async def generator():
        async for chunk in chat.response_stream():
            yield chunk

    return Response(generator(), mimetype='text/event-stream', content_type='text/event-stream')


@chatbot.route('/test_ne', methods=['GET'])
def test_ne():
  import requests
  data = {
      "userid": 2
  }
  headers = {
      "Accept-Charset": "",
      "Content-Type": "application/json",
      "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3MzIyNjg5NDIsImp0aSI6IjAxMGFlMDIyLWE4YjctMTFlZi1iZGM1LTAyNDJhYzE0MDAwMyIsImlzcyI6ImxvY2FsaG9zdCIsIm5iZiI6MTczMjI2ODk0MiwiZXhwIjoxNzMyODczNzQyLCJ1c2VyaWQiOiIyIn0.-KEJj58RJT4m0YR502TQQ37zP_pyQfSUrIYtNlL33-V7U0-zimmP_oeLT6e1ZVvNaNQdQdBc04EtnF8YRB3d5Q",
  }

  url = "http://10.10.10.14:8009/api/integrated/ai/student-course"
  try:
    response = requests.get(url, json=data, headers=headers)
    return str(response.json()['data'])
  except Exception as e:
    return str(e)