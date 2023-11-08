from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.vectorstores.redis import Redis

load_dotenv('.env')

def connect_redis_db():
    embedding = HuggingFaceHubEmbeddings()
    redis_url = "redis://localhost:6379"
    index_name = 'test'
    index_schema = {
        "tag": [{"name": "credit_score"}],
        "text": [{"name": "user"}, {"name": "job"}],
        "numeric": [{"name": "age"}],
    }
    vectorstore = Redis.from_existing_index(
        embedding=embedding,
        index_name=index_name,
        redis_url=redis_url,
        schema=index_schema
    )
    return vectorstore

def get_conversation_chain(question):
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0)
    vectorstore = connect_redis_db()
    memory = ConversationBufferMemory(
    memory_key='chat_history', return_messages=True)

    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation({'question': question})
    