from llm.factory.training.training import Training
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from pathlib import Path
class TrainingCourse(Training):
    def __init__(self):
        super().__init__()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        self.columns = ['title','content','courseid','source']
        self.context = "course"

    def save_training_data(self,data):
        finaldocx = []
        path = Path(data['source'])
        typefile = path.suffix.lower()
        try:
            
            if typefile == '.pdf':
                docs = PyPDFLoader(data['source'])
            else:
                docs = UnstructuredURLLoader(urls=[data['source']])

            all_splits = self.text_splitter.split_documents(docs.load())

            metadata = {}
            for key,value in data.items():
                if key in self.columns:
                    metadata[key] = value
            for doc in all_splits:
                finaldocx.append(Document(page_content=doc.page_content,metadata=metadata))

            self.vector_db.add_vectordb(finaldocx,self.context+'_'+data['collection'])

            return 'Training Thành công'
        
        except:
            return 'Training Thất bại'


    def update_training_data(self):
        pass

    def check_training_duplication(self):
        pass
    
    def summary_traning_data(self):
        pass