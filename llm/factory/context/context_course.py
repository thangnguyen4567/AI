from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from llm.factory.context.context import Context
class ContextCourse(Context):
    def __init__(self):
        super().__init__()
        self.prompt = """
            - Bạn là AI trợ giảng Elearning Pro, hỗ trợ trả lời những thông tin trong khóa học
            - Nếu được hỏi về tớm tắt tài liệu bản chỉ cần trả lời theo bản tóm tắt được tóm tắt sẵn bên dưới (nếu có)
            - Khóa học học có những nội dung như sau:
        """
        self.context = "course"
        self.documents = []
        self.index_schema = {
                                "text": [
                                    {"name":"source"},
                                    {"name":"title"},
                                    {"name":"content"},
                                ],
                                "numeric": [
                                    {"name":"courseid"},
                                    {"name":"coursemoduleid"},
                                ]
                            }
        self.docsretriever = 4

    def retriever_document(self,contextdata: dict,question: str) -> str:
        if 'courseid' in contextdata and 'title' in contextdata:
            filter = RedisFilter.num('coursemoduleid') == int(contextdata['coursemoduleid'])
            self.documents = VectorDB().connect_vectordb(index_name=self.context+'_'+contextdata['collection'],index_schema=self.index_schema).similarity_search(question,k=self.docsretriever,filter=filter)
            if self.documents:
                for doc in self.documents:
                    self.prompt += doc.page_content
        return self.prompt