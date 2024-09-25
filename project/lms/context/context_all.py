from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from factory.base.context import Context

class ContextLMS(Context):
    def __init__(self):
        self.prompt = """
            Bạn là AI trợ giảng Elearning Pro, được thiết kế để hỗ trợ người dùng trong việc trả lời các câu hỏi liên quan đến tài liệu hướng dẫn sử dụng và tài liệu trong khóa học.
            Nếu người dùng hỏi về một tài liệu cụ thể, hãy tóm tắt những ý chính của tài liệu đó
            Khi cung cấp câu trả lời, nếu có tài liệu tham khảo hoặc nguồn tài liệu hoặc link khóa học, hãy hiển thị chúng dưới dạng thẻ a với target="_blank".
            Hãy trả lời một cách linh hoạt, tùy thuộc vào ngữ cảnh và thông tin mà người dùng cần. Nếu câu hỏi không rõ ràng, hãy hỏi lại để làm rõ.
            Nội dung hỗ trợ bao gồm 3 nhóm chính:
            1. **Tài liệu khóa học**: Bao gồm các tài liệu học tập, bài giảng, và tài liệu liên quan trực tiếp đến các khóa học.
            2. **Hướng dẫn sử dụng hệ thống**: Hướng dẫn về cách sử dụng hệ thống LMS của 3 vai trò học viên,giáo viên,quản lý đào tạo
            3. **Thông tin khóa học**: Thông tin chi tiết về các khóa học như Tên,section,danh sách các tài nguyên,hoạt động trong khóa
        """
        self.prompt = """
            Bạn là AI trợ giảng Elearning Pro, được thiết kế để hỗ trợ người dùng trong việc trả lời các câu hỏi về hệ thống LMS, bao gồm các hướng dẫn sử dụng và tài liệu trong khóa học.
            Nhiệm vụ của bạn là cung cấp câu trả lời chính xác, dễ hiểu, và phù hợp với ngữ cảnh của câu hỏi.
            - Nếu người dùng hỏi về một tài liệu cụ thể, hãy tóm tắt những ý chính và giải thích cách sử dụng tài liệu đó trong ngữ cảnh học tập.
            - Nếu có các tài liệu tham khảo, nguồn tài liệu, hoặc đường dẫn khóa học, hãy cung cấp chúng dưới dạng thẻ <a> với target="_blank" để người dùng có thể mở trong tab mới.
            - Nếu câu hỏi không rõ ràng hoặc cần thêm thông tin, hãy hỏi lại người dùng để làm rõ trước khi đưa ra câu trả lời.
            - Hãy luôn linh hoạt trong cách trả lời để phù hợp với nhu cầu của người dùng và đảm bảo câu trả lời ngắn gọn, súc tích khi cần.
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
                    'Câu hỏi về các tài liệu,tóm tắt tài liệu nằm trong lớp học,khóa học,thông tin không liên quan đến các thông tin của các chủ đề trên'
                ),
            },
            {
                'title': 'course',
                'priority': '2',
                'description': (
                    'Câu hỏi liên quan đến khóa,khóa học,lớp học > tìm kiếm khóa học, tóm tắt khóa học...'
                ),
            }
        ]

    def retriever_document(self,contextdata: dict,question: str) -> str:
        
        topics = self.classify_topic(question, self.topics)

        for topic in topics:
            if topic.strip() in ['student', 'manager', 'teacher']:
                combined_filter = RedisFilter.text("role") == topics[0].strip()
                
                for item in topics[1:]:
                    combined_filter |= RedisFilter.text("role") == item.strip()

                self.index_schema = {
                    "text": [
                        {"name":"title"},
                        {"name":"role"},
                        {"name":"content"}
                    ],
                }

                self.documents.extend(VectorDB().connect_vectordb(index_name='system', index_schema=self.index_schema).similarity_search(question, k=4, filter=combined_filter))

            if topic.strip() in ['resource']:

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
                self.documents.extend(VectorDB().connect_vectordb(index_name='resource_'+contextdata['collection'],index_schema=self.index_schema).similarity_search(question,k=8))

            if topic.strip() in ['course']:
                
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

                self.documents.extend(VectorDB().connect_vectordb(index_name='course_'+contextdata['collection'],index_schema=self.index_schema).similarity_search(question,k=4))

        if self.documents:
            for doc in self.documents:
                self.prompt += doc.page_content
                if 'source' in doc.metadata and doc.metadata['source']:
                    if 'coursemoduleid' in doc.metadata:
                        self.prompt += 'Nguồn tài liệu:' + doc.metadata['source'] + '.\n'
                    else:
                        self.prompt += 'Link khóa học:' + doc.metadata['source'] + '--Hết thông tin khóa học--.\n'

        return self.prompt