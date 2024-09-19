from factory.base.training import Training
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredURLLoader,SeleniumURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema import Document
from langchain_community.vectorstores.redis import RedisFilter
from pathlib import Path
import os

class TrainingCourse(Training):
    def __init__(self):
        super().__init__()

        #google_api_key = os.getenv("GOOGLE_API_KEY_SUMMARY")
        #self.llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.columns = ['title','content','coursemoduleid','courseid','source','coursename']
        self.context = "course"

    def save_training_data(self,data):

        finaldocx = []
        path = Path(data['source'])
        typefile = path.suffix.lower()
        db = self.context+'_'+data['collection']
        try:
            
            if typefile == '.pdf':
                docs = PyPDFLoader(data['source'])
                text = ''
                for doc in docs.load():
                    text += doc.page_content
                all_splits = [Document(page_content=split, metadata={}) for split in self.text_splitter.split_text(text)]

            else:
                docs = UnstructuredURLLoader(urls=[data['source']])
                all_splits = self.text_splitter.split_documents(docs.load())

            metadata = {}

            for key,value in data.items():
                if key in self.columns:
                    metadata[key] = value
                    
            for doc in all_splits:
                content = 'Tài liệu: ' + metadata['title']
                content += 'Thuộc lớp học: ' + metadata['coursename'] 
                content += doc.page_content
                finaldocx.append(Document(page_content=content,metadata=metadata))

            
            ## Xử lý lưu docs tóm tắt tài liệu
            # summary = 'Bản tóm tắt tài liệu '+data['title']+':' + self.summary_traning_data(all_splits)
            # finaldocx.append(Document(page_content=summary,metadata=metadata))

            self.vector_db.add_vectordb(finaldocx,db)

            self.reponse['message'] = 'Training thành công'

            return self.reponse
        
        except Exception as e:

            print(str(e))

            self.reponse['error'] = True
            self.reponse['message'] = f'Training thất bại: {str(e)}'

            return self.reponse

    def check_training_duplication(self):
        pass
    
    def summary_traning_data(self,docs):
        
        summary = 'Bản tóm tắt tài liệu và các ý chính:'
        content = ''
        num_tokens = 0

        for doc in docs:
            num_tokens += len(doc.page_content)/4
            if(num_tokens < 25000):
                content += doc.page_content
            else:
                break

        summary += self.llm.invoke(input="""Bạn hãy tóm tắt tài liệu sau đây giúp tôi nhé, tài liệu:
            {content}
        """.format(content=content))
        return summary