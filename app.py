from fastapi import FastAPI
from Model.questionModel import Question
from Controller.answerController import get_conversation_chain
app = FastAPI()

@app.post("/api/conversations")
async def create_item(request: Question):
    conversation = get_conversation_chain(request.question)
    chat_history = conversation['chat_history']
    reponse = {}
    for i, message in enumerate(chat_history):
        if i % 2 == 0:
            reponse["question"] = message.content
        else:
            reponse["answer"] = message.content
            
    return reponse

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8181)