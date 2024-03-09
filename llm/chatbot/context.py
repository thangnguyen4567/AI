from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
class Context():
    def __init__(self):
        self.course_index_schema = {
            "text": [{"name": "courseid"}],
        }
        self.system_index_schema = {
            "text": [{"name": "role"},{"name": "source"},{"name": "title"}],
        }
        self.prompt = ''
        self.documents = []

    def course_context(self) -> None:
        self.prompt = """
            Bạn là AI trợ giảng Elearning Pro, hỗ trợ trả lời những thông tin trong khóa học
            - Khóa học học có những nội dung như sau:
        """

    def system_context(self) -> None:
        self.prompt = """
            - Bạn là trợ lý ảo Elearning Pro hỗ trợ trả lời hướng dẫn sử dụng các chức năng trên hệ thống
            - Đối với những câu hỏi về tra cứu tài liệu , chức năng trên hệ thống nếu không tìm thấy tài liệu liên quan đến câu trả lời thì nên trả lời: Xin lỗi tôi không tìm thấy tài liệu theo yêu cầu của bạn
            - Tài liệu hướng dẫn sử dụng hệ thống bao gồm những chức năng sau:
        """

    def main_context(self) -> None:
        self.prompt = """
            - Bạn là trợ lý ảo Elearning Pro hỗ trợ trả lời những thông tin trên hệ thống
            - Khi trả lời câu hỏi bạn không nên đề cập đến chữ moodle
        """

    def retriever_document(self) -> None:
        prompt = ''
        filter = ''
        method_name = self.context+'_index_schema'
        if(hasattr(self,method_name)):
            index_schema = getattr(self,method_name)
            for value in self.contextdata:
                filter = RedisFilter.text(value) == self.contextdata[value]
            if filter != '':
                self.documents = VectorDB().connect_vectordb(index_name=self.context,index_schema=index_schema).similarity_search(self.question,k=4,filter=filter)
            if self.documents:
                prompt += self.documents[0].page_content
        return prompt
        
    def get_context(self) -> str:
        method_name = self.context + "_context"
        if(hasattr(self,method_name)):
            method = getattr(self, method_name)
            method()
        return self.prompt
    

    