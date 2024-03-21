from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from llm.factory.context.context import Context
class ContextSystem(Context):
    def __init__(self):
        super().__init__()
        self.prompt = """
            - Bạn là trợ lý ảo Elearning Pro hỗ trợ trả lời hướng dẫn sử dụng các chức năng trên hệ thống
            - Đối với những câu hỏi về tra cứu tài liệu , chức năng trên hệ thống nếu không tìm thấy tài liệu liên quan đến câu trả lời thì nên trả lời: Xin lỗi tôi không tìm thấy tài liệu theo yêu cầu của bạn
            - Tài liệu hướng dẫn sử dụng hệ thống bao gồm những chức năng sau:
        """
        self.documents = []
        self.context = 'system'
        self.index_schema = {
                                "text": [
                                    {"name":"source"},
                                    {"name":"title"},
                                    {"name":"role"},
                                    {"name":"content"}
                                ],
                            }
        self.docsretriever = 5
    
    def retriever_document(self,contextdata,question) -> str:
        if 'role' in contextdata:
            filter = RedisFilter.text('role') == contextdata['role']
            self.documents = VectorDB().connect_vectordb(index_name=self.context,index_schema=self.index_schema).similarity_search(question,k=self.docsretriever,filter=filter)
            if self.documents:
                self.prompt += self.documents[0].page_content
        return self.prompt