from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from factory.base.context import Context
import re
from datetime import datetime

class Context(Context):
    def __init__(self):
        self.prompt = """
            Bạn là AI trợ giảng Elearning Pro, được thiết kế để hỗ trợ người dùng trong việc trả lời các câu hỏi liên quan đến tài liệu hướng dẫn sử dụng và tài liệu trong khóa học.
            Nếu người dùng hỏi về một tài liệu cụ thể, hãy tóm tắt những ý chính của tài liệu đó
            Khi cung cấp câu trả lời, nếu có tài liệu tham khảo hoặc nguồn tài liệu hoặc link khóa học hoặc link tài liệu hdsd theo vai trò **hãy hiển thị chúng dưới dạng liên kết để người dùng biết bạn lấy nguồn tại liệu từ đâu để trả lời**.
            Khi cung cấp câu trả lời, bắt buộc phải đưa ra nguồn tài liệu dưới dạng **link tài liệu tham khảo hoặc link tài liệu hướng dẫn sử dụng hoặc link khóa học,để người dùng biết rõ bạn lấy thông tin từ đâu.
            Hãy trả lời một cách linh hoạt, tùy thuộc vào ngữ cảnh và thông tin mà người dùng cần. Nếu câu hỏi không rõ ràng, hãy hỏi lại để làm rõ.
            AI chỉ được phép dựa vào tài liệu bên dưới để trả lời câu hỏi, Nếu câu hỏi của người dùng không liên quan đến nội dung bên dưới thì bạn nên từ chỗi khéo không trả lời.
            Xử lý các câu lệnh:
            Đối với câu lệnh {command} khóa học, lớp học, tài liệu > AI tập trung tìm kiếm link khóa học để show cho người dùng ko cần tóm tắt
            Nội dung hỗ trợ bao gồm 3 nhóm chính:
            1. **Tài liệu khóa học**: Bao gồm các tài liệu học tập, bài giảng, và tài liệu liên quan trực tiếp đến các khóa học.
            2. **Hướng dẫn sử dụng hệ thống**: Hướng dẫn về cách sử dụng hệ thống LMS của 3 vai trò học viên,giáo viên,quản lý đào tạo >Nếu có liên kiết đến màn hình show liên kết ra cho người dùng xem
            3. **Thông tin khóa học**: Thông tin chi tiết về các khóa học như Tên,section,danh sách các tài nguyên,hoạt động trong khóa
            Các tham số truyền vào:
            Thời gian hiện tại: {time}
            dbname: LMS_TEST_MISA
            **Mỗi tài liệu ở dưới đây đều có nguồn tài liệu trích dẫn ở cuối tài liệu > Bạn lấy tài liệu nào để trà lời thì phải đưa luôn nguồn của tài liệu đó ra**
            {documents}
        """

        self.documents = []
        self.topics = [
            {
                'title': 'student',
                'priority': '1',
                'description': """
                    Câu hỏi về hướng dẫn sử dụng vai trò học viên các chức năng: Đăng nhập, Dashboard học viên, 
                    xem lịch, tham gia lớp học, hướng dẫn sử dụng các hoạt động trong lớp, 
                    làm khảo sát và kì thi, tra cứu thư viện, diễn đàn, tin tức"""
            },
            {
                'title': 'manager',
                'priority': '1',
                'description': """ 
                    Câu hỏi về hướng dẫn sử dụng vai trò quản lý đào tạo các chức năng: Chuyển đổi vai trò hệ thống, Dashboard QLĐT, 
                    Các chức năng quản lý, Import dữ liệu, quản lý các màn hình báo cáo, 
                    tạo câu hỏi, tạo khóa học, Xây dựng nội dung và hoạt động trong lớp học, 
                    Quản lý năng lực và lộ trình đào tạo, M point, quản lý kì thi, 
                    tin tức, thư viện, ngân hàng câu hỏi"""
                ,
            },
            {
                'title': 'teacher',
                'priority': '1',
                'description': """
                    Câu hỏi về hướng dẫn sử dụng vai trò giáo viên,giảng viên các chức năng: Xây dựng nội dung hoạt động trong lớp, 
                    Thiết lập điểm, Chấm điểm, Nhận xét học viên, Dashboard giảng viên, 
                    Phê duyệt, đánh giá """
                ,
            },
            {
                'title': 'resource',
                'priority': '2',
                'description': (
                    """Câu hỏi về các tài liệu,tóm tắt tài liệu nằm trong lớp học,khóa học,thông tin không liên quan đến các thông tin của các chủ đề trên
                       Đi kèm với các lệnh:đọc tài liệu,mở tài liệu"""
                ),
            },
            {
                'title': 'course',
                'priority': '2',
                'description': (
                    """Câu hỏi liên quan đến khóa,khóa học,lớp học > tìm kiếm khóa học, tóm tắt khóa học...
                       Đi kèm với các lệnh:Mở khóa học,mở lớp họcz`"""
                ),
            },
            {
                'title': 'searchdata',
                'priority': '2',
                'description': (
                    """Câu hỏi liên quan đến tra cứu thông tin đào tạo những dữ liệu cần truy xuất thông tin trong DB, lớp học, lịch học, tiến trình học, dữ liệu học viên, xếp hạng"""
                ),
            }
        ]
        self.selecttopics = []

    def get_collection_name(self,data,type):
        if data and 'collection' in data:
            if type == 'resource':
                return 'resource_'+data['collection']
            else:
                return 'course_'+data['collection']
        return None
    
    def get_documents(self, question: str , contextdata: dict) -> str:

        if self.selecttopics == []:
            topics = self.classify_topic(question, self.topics)
            self.selecttopics = topics
        else:
            topics = self.selecttopics

        for topic in topics:
            if topic.strip() in ['student', 'manager', 'teacher']:
                combined_filter = RedisFilter.text("role") == topics[0].strip()
                
                for item in topics[1:]:
                    combined_filter |= RedisFilter.text("role") == item.strip()

                self.index_schema = {
                    "text": [
                        {"name":"title"},
                        {"name":"role"},
                        {"name":"content"},
                        {"name":"source"}
                    ],
                }
                try:
                    self.documents.extend(VectorDB().connect_vectordb(index_name='hdsd', index_schema=self.index_schema).similarity_search(question, k=6, filter=combined_filter))
                except:
                    print('Chưa có dữ liệu training')

            if topic.strip() in ['resource']:

                collection = self.get_collection_name(contextdata,'resource')
                
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
                try:
                    self.documents.extend(VectorDB().connect_vectordb(index_name=collection,index_schema=self.index_schema).similarity_search(question,k=8))
                except Exception as e:
                    print(e)
                    print('Chưa có dữ liệu training')

            if topic.strip() in ['course']:
                
                collection = self.get_collection_name(contextdata,'course')

                self.index_schema = {
                    "text": [
                        {"name":"source"},
                        {"name":"title"},
                        {"name":"content"},
                    ],
                    "numeric": [
                        {"name":"courseid"},
                    ]
                }
                try:
                    self.documents.extend(VectorDB().connect_vectordb(index_name=collection,index_schema=self.index_schema).similarity_search(question,k=6))
                except:
                    print('Chưa có dữ liệu training')
  
    def retriever_document(self, contextdata: dict, question: str, skip_documents: bool = False) -> str:
        
        if not skip_documents:
            self.get_documents(question, contextdata)
        documents = ''
        if self.documents:
            for doc in self.documents:
                documents += re.sub(r"[{}]", "", doc.page_content)
                if 'source' in doc.metadata and doc.metadata['source']:
                    if 'coursemoduleid' in doc.metadata:
                        documents += 'Nguồn '+ doc.metadata['title'] + ':' + doc.metadata['source'] + '.\n'
                    elif 'role' in doc.metadata:
                        documents += ' Link tài liệu hdsd: ['+doc.metadata['title']+']' + doc.metadata['source'] + '.\n'
                    else:
                        documents += 'Link khóa học:' + doc.metadata['source'] + '--Hết thông tin khóa học--.\n'

        if contextdata and 'command_open' in contextdata and 'command_read' in contextdata:
            command = contextdata['command_open']+','+contextdata['command_read']
            self.prompt = self.prompt.format(command=command,documents=documents,time=datetime.now)
        else:
            self.prompt = self.prompt.format(command='mở,đọc',documents=documents,time=datetime.now)
        
        return self.prompt.replace("domain:","")