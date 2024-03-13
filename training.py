from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.config_vectordb import VectorDB
from langchain.schema import Document
load_dotenv()

# pdf = PyPDFLoader("./document/Ky nang dong vien nhan vien.pdf")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)

finaldocx = []
docx = PyPDFLoader("./document/Ky nang dong vien nhan vien.pdf")
all_splits = text_splitter.split_documents(docx.load())
for doc in all_splits:
    finaldocx.append(Document(page_content=doc.page_content,metadata={'context':'course',
                                                                      'role':'student',
                                                                      'title': 'Kỹ năng động viên nhân viên',
                                                                      'courseid':'70373',
                                                                      'source':doc.metadata['source']}))
VectorDB().add_vectordb(finaldocx,'course')

