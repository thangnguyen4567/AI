from factory.base.training import Training
from langchain.schema import Document

class TrainingCourse(Training):
    def __init__(self):
        super().__init__()
        self.columns = ['title','content','courseid','source','categoryid','categoryname']
        self.redis_client = self.vector_db.connect_client()

    def save_training_data(self,data):

        collection = 'course_'+data['collection']

        try:
            metadata = {}
            for key,value in data.items():
                if key in self.columns:
                    metadata[key] = value

            for key in self.redis_client.scan_iter("doc:"+collection+"*"):
                courseid = self.redis_client.hget(key,'courseid').decode()
                if courseid == metadata['courseid']:
                    self.redis_client.delete(key)
            
            document = Document(page_content=metadata['content'],metadata=metadata)

            self.vector_db.add_vectordb([document],collection)

            self.reponse['error'] = False
            self.reponse['message'] = 'Training thành công'

            return self.reponse
        
        except Exception as e:

            print(str(e))

            self.reponse['error'] = True
            self.reponse['message'] = f'Training thất bại: {str(e)}'

            return self.reponse

    def delete_training_data(self,data):

        collection = 'course_'+data['collection']

        try:
            courseids_set = set(data['courseids'])
            keys_to_delete = []

            for key in self.redis_client.scan_iter("doc:"+collection+"*"):
                courseid_redis = self.redis_client.hget(key, 'courseid').decode()
                if courseid_redis in courseids_set:
                    keys_to_delete.append(key)

            if keys_to_delete:
                self.redis_client.delete(*keys_to_delete)

            self.reponse['error'] = False
            self.reponse['message'] = 'Xóa khóa học thành công'

            return self.reponse
        
        except Exception as e:

            print(str(e))
            self.reponse['error'] = True
            self.reponse['message'] = f'Xóa khóa học thất bại: {str(e)}'

            return self.reponse


    def check_training_duplication(self):
        pass