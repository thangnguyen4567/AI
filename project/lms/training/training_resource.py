from factory.base.training import Training
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from pathlib import Path

class TrainingResource(Training):
    def __init__(self):
        super().__init__()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.columns = ['title','content','coursemoduleid','courseid','source','coursename']
        self.redis_client = self.vector_db.connect_client()

    def save_training_data(self,data):

        finaldocx = []
        path = Path(data['source'])
        typefile = path.suffix.lower()
        collection = 'resource_'+data['collection']

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
                    
            for key in self.redis_client.scan_iter("doc:"+collection+"*"):
                coursemoduleid = self.redis_client.hget(key,'coursemoduleid').decode()
                if coursemoduleid == metadata['coursemoduleid']:
                    self.redis_client.delete(key)
                    
            for doc in all_splits:
                content = 'Tài liệu: ' + metadata['title']
                content += 'Thuộc lớp học: ' + metadata['coursename'] 
                content += doc.page_content
                finaldocx.append(Document(page_content=content,metadata=metadata))

            self.vector_db.add_vectordb(finaldocx,collection)

            self.reponse['error'] = False
            self.reponse['message'] = 'Training thành công'

            return self.reponse
        
        except Exception as e:

            print(str(e))

            self.reponse['error'] = True
            self.reponse['message'] = f'Training thất bại: {str(e)}'

            return self.reponse


    def delete_training_data(self,data):

        collection = 'resource_'+data['collection']

        try:
            coursemoduleids_set = set(data['coursemoduleids'])
            keys_to_delete = []

            for key in self.redis_client.scan_iter("doc:"+collection+"*"):
                coursemoduleid_redis = self.redis_client.hget(key, 'coursemoduleid').decode()
                if coursemoduleid_redis in coursemoduleids_set:
                    keys_to_delete.append(key)

            if keys_to_delete:
                self.redis_client.delete(*keys_to_delete)

            self.reponse['error'] = False
            self.reponse['message'] = 'Xóa dữ liệu thành công'

            return self.reponse
                        
        except Exception as e:

            print(str(e))
            self.reponse['error'] = True
            self.reponse['message'] = f'Xóa dữ liệu thất bại: {str(e)}'

            return self.reponse
        
    def check_training_duplication(self):
        pass