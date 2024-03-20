from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
class ContextCourse():
    def __init__(self):
        self.prompt = """
            - Bạn là AI trợ giảng Elearning Pro, hỗ trợ trả lời những thông tin trong khóa học
            - Khóa học học có những nội dung như sau:
        """
        self.context = "course"
        self.documents = []
        self.index_schema = {
                                "text": [
                                    {"name":"source"},
                                    {"name":"title"},
                                    {"name":"content"},
                                    {"name":"role"},
                                ],
                                "numeric": [
                                    {"name":"courseid"}
                                ]
                            }
        self.docsretriever = 5

    def retriever_document(self,contextdata,question) -> str:
        if 'courseid' in contextdata and 'title' in contextdata:
            filtertitle = RedisFilter.text('title') == contextdata['title'] 
            filtercourseid = RedisFilter.num('courseid') == int(contextdata['courseid'])
            filter = filtertitle & filtercourseid
            self.documents = VectorDB().connect_vectordb(index_name=self.context,index_schema=self.index_schema).similarity_search(question,k=self.docsretriever,filter=filter)
            if self.documents:
                for doc in self.documents:
                    self.prompt += doc.page_content
        return self.prompt