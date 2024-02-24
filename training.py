from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from config.config_vectordb import VectorDB
from langchain.schema import Document
load_dotenv()

docx = Docx2txtLoader("./document/24.kynangdamphan.docx")
pdf = PyPDFLoader("./document/Ky nang dong vien nhan vien.pdf")
raw_docx = docx.load()
raw_pdf = pdf.load()
finaldocx = []
finalpdf = []
for doc in raw_docx:
    finaldocx.append(Document(page_content=doc.page_content,metadata={'courseid':70373}))
for pdf in raw_pdf:
    finalpdf.append(Document(page_content=pdf.page_content,metadata={'courseid':6}))
VectorDB().add_vectordb(finaldocx,'chatbot')
VectorDB().add_vectordb(finalpdf,'chatbot')