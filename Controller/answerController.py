from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceHubEmbeddings,OpenAIEmbeddings
from langchain.vectorstores.redis import Redis
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import faiss

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

def connect_vectorstore_db():
    embeddings = OpenAIEmbeddings()
    raw_documents = DirectoryLoader('./document', glob="**/*").load()
    text_splitter = CharacterTextSplitter(separator="\n",
                                        chunk_size=1000,
                                        chunk_overlap=200,
                                        length_function=len)
    documents = text_splitter.split_documents(raw_documents)
    vectorstore = faiss.FAISS.from_documents(documents=documents, embedding=embeddings)
    return vectorstore
    
    
def get_conversation_chain():
    vectorstore = connect_vectorstore_db()
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0)
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
    )
    return conversation
    