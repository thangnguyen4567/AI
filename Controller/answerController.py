from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.redis import Redis
from langchain.document_loaders import DirectoryLoader,PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter,TokenTextSplitter
from langchain.vectorstores import faiss

load_dotenv('.env')

def connect_vectorstore_db():
    embeddings = OpenAIEmbeddings(disallowed_special=())
    raw_documents = DirectoryLoader('./document', glob="**/*.pdf").load()
    text_splitter = CharacterTextSplitter(separator="\n",
                                        chunk_size=1000,
                                        chunk_overlap=200,
                                        length_function=len)
    documents = text_splitter.split_documents(raw_documents)
    vectorstore = faiss.FAISS.from_documents(documents=documents, embedding=embeddings)
    return vectorstore
    
    
def get_conversation_chain():
    vectorstore = connect_vectorstore_db()
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0,openai_api_key="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")
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
    )
    return conversation
    