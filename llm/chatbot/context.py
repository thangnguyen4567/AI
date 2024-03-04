from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
class Context():
    def __init__(self):
        self.course_index_schema = {
            "text": [{"name": "courseid"}],
        }
        self.system_index_schema = {
            "text": [{"name": "guide"},{"name": "source"}],
        }
        self.context = ''

    def course_context(self) -> None:
        self.context = """
            Bạn là AI trợ giảng Elearning Pro ( Được làm dựa hệ thống moodle ), hỗ trợ trả lời những thông tin trong khóa học
            - Khóa học học có những nội dung như sau:
        """

    def system_context(self) -> None:
        self.context = """
            - Bạn là trợ lý ảo Elearning Pro hỗ trợ trả lời những thông tin trên hệ thống
            - Khi trả lời câu hỏi bạn không nên đề cập đến chữ moodle
            - Tài liệu hướng dẫn sử dụng hệ thống bao gồm những thông tin sau:
        """

    def main_context(self) -> None:
        self.context = """
            - Bạn là trợ lý ảo Elearning Pro ( Được làm dựa hệ thống moodle , bạn có thể tham khảo tài liệu hướng dẫn sử dụng của moodle để trả lời ), hỗ trợ trả lời những thông tin trên hệ thống
            - Khi trả lời câu hỏi bạn không nên đề cập đến chữ moodle
        """

    def retriever_document(self,question: str,contextdata, context: str) -> None:
        prompt = ''
        method_name = context+'_index_schema'
        if(hasattr(self,method_name)):
            index_schema = getattr(self,method_name)
            for value in contextdata:
                filter = RedisFilter.text(value) == contextdata[value]
            documents = VectorDB().connect_vectordb(index_name=context,index_schema=index_schema).similarity_search(question,k=5,filter=filter)
            for value in documents:
                prompt += value.page_content
        return prompt
        
    def get_context(self,context: str) -> None:
        method_name = context + "_context"
        if(hasattr(self,method_name)):
            method = getattr(self, method_name)
            method()
        return self.context
    

    