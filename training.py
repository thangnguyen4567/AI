from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.config_vectordb import VectorDB
from langchain.schema import Document
load_dotenv()

# pdf = PyPDFLoader("./document/Ky nang dong vien nhan vien.pdf")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
# all_splits = text_splitter.split_documents(docx.load())
finaldocx = []
docx = Docx2txtLoader("./document/TAILIEU_HDSD_GV_LMS4.0.docx")
all_splits = text_splitter.split_documents(docx.load())
for doc in all_splits:
    finaldocx.append(Document(page_content=doc.page_content,metadata={'context':'system','guide':'teacher'}))
VectorDB().add_vectordb(finaldocx,'system_guide')

finaldocx = []
docx = Docx2txtLoader("./document/TAILIEU_HDSD_hv_LMS4.0.docx")
all_splits = text_splitter.split_documents(docx.load())
for doc in all_splits:
    finaldocx.append(Document(page_content=doc.page_content,metadata={'context':'system','guide':'student'}))
VectorDB().add_vectordb(finaldocx,'system_guide')

finaldocx = []
docx = Docx2txtLoader("./document/TAILIEU_HDSD_QLDT_LMS4.0.docx")
all_splits = text_splitter.split_documents(docx.load())
for doc in all_splits:
    finaldocx.append(Document(page_content=doc.page_content,metadata={'context':'system','guide':'manager'}))
VectorDB().add_vectordb(finaldocx,'system_guide')

finaldocx = []
docx = Docx2txtLoader("./document/TAILIEU_HDSD_QTV_LMS4.0.docx")
all_splits = text_splitter.split_documents(docx.load())
for doc in all_splits:
    finaldocx.append(Document(page_content=doc.page_content,metadata={'context':'system','guide':'admin'}))
VectorDB().add_vectordb(finaldocx,'system_guide')

# VectorDB().add_vectordb(finalpdf,'chatbot')