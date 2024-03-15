from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from langchain_community.vectorstores.redis import RedisText
class Context():
    def __init__(self):
        self.prompt = ''
        self.documents = []
        self.index_schema = {
                                "text": [{"name":"source"},{"name":"title"}],
                                "numeric": []
                            }
        self.k = {"system": 4, "course": 5}

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

    def retriever_document(self) -> None:
        ## Xử lý filter dữ liệu theo metadata
        filtertext = ''
        filternumber = ''
        filter = ''
        for key, value in self.contextdata.items():
            if value.isnumeric():
                filternumber = RedisFilter.num(key) == int(value)
                self.index_schema["numeric"].append({"name": key})
            else:
                filtertext = RedisFilter.text(key) == value
                self.index_schema["text"].append({"name": key})

        if(filtertext and filternumber):
            filter = filtertext & filternumber
        elif(filtertext):
            filter = filtertext
        elif(filternumber):
            filter = filternumber
        if filter != '':
            self.documents = VectorDB().connect_vectordb(index_name=self.context,index_schema=self.index_schema).similarity_search(self.question,k=self.k[self.context],filter=filter)
        if self.documents:
            if self.context == 'course':
                for doc in self.documents:
                    self.prompt += doc.page_content
            elif self.context == 'system':
                self.prompt += self.documents[0].page_content
        
    def get_context(self) -> str:
        method_name = self.context + "_context"
        if(hasattr(self,method_name)):
            method = getattr(self, method_name)
            method()
        return self.prompt
    

    