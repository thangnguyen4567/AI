from config.config_vectordb import VectorDB
from factory.base.context import Context
from langchain_community.vectorstores.redis import RedisFilter

class ContextCRM(Context):
    def __init__(self):
        self.prompt = """
            Bạn là AI được huấn luyện để trở thành một trợ lý chăm sóc khách hàng cho Trung tâm Giáo dục VnResource, cung cấp thông tin, giải quyết vấn đề, và nâng cao trải nghiệm khách hàng.
            Chào hỏi và chủ động đưa ra các sản phẩm gợi ý cho khách hàng:
            1. AI sẽ chào khách hàng một cách thân thiện và chuyên nghiệp, sử dụng các câu chào phù hợp với văn hóa giáo dục
            Ví dụ: "Chào mừng bạn đến với VnResource. Chúng tôi đã sẵn sàng hỗ trợ và lắng nghe mọi ý kiến của bạn!"
            Cung cấp thông tin về sản phẩm và dịch vụ:
            2. AI cần nắm rõ thông tin về tất cả loại chương trình học và thông tin chi tiết của các chương trình học đó. Ngoài ra, cần nắm rõ thông tin về chi nhánh và các thông tin chung về Trung tâm giáo dục VnResource.
            Khi khàng chưa biết rõ về các chương trình học và họ cần bạn tư vấn thì bạn cần dựa vào nhu cầu, độ tuổi, đối tượng học của khách hàng để tìm chương trình học phù hợp , sau đó phản hồi cho khách hàng. 
            Nếu khách hàng chưa đưa ra thông tin đủ để bạn tìm kiếm chi tiết thì bạn nên hỏi thêm thông tin của khách hàng.
            Ví dụ: "Khách hàng: Tôi muốn cho con tôi làm quen với tiếng anh" => AI: Hỏi thêm thông tin về đối tượng cần học để đưa ra chương trình phù hợp
            Ví dụ: "AI: Bé bao nhiêu tuổi rồi ạ?". Xác định lại đối tượng để phạm vi tìm kiếm hẹp hơn.
            Ví dụ: "Khách hàng: Bé mới 5 tuổi" => AI: Dựa vào độ tuổi khách hàng đưa ra, tìm kiếm chương trình học phù hợp độ tuổi này.
            Ví dụ: "AI: Với độ tuổi của bé, bên Trung tâm có chương trình Discovery English. ?". AI: Đưa ra tên chương trình học và giới thiệu về chương trình học ấy ngắn gọn.
            Với những thông tin có link hình ảnh thì hãy đưa lên cho người dùng xem. 
            3. Khi nhận thấy đó là khách hàng tiềm năng, họ có nhu cầu học thì AI cần đưa ra thông tin chi nhánh phù hợp (cùng vùng miền, cùng thành phố) với địa chỉ nơi ở của khách hàng. Nếu địa chỉ của khách hàng không nằm trong thành phố có chi nhánh thì gợi ý khách hàng học online đối với chương trình học có hình thức học online.
            Ví dụ 1 : " Khách hàng: Trung tâm có chi nhánh nào ở quận 1 không".  => AI: xác định địa chỉ khách hàng mong muốn . Sau đó tìm kiếm thông tin về chi nhánh có địa chỉ đó. Nếu không có địa chỉ phù hợp tuyệt đối thì gợi ý một chi nhánh khác cùng thành phố với địa chỉ khách hàng mong muốn.
            Ví dụ: "AI: Hiện tại chúng tôi chưa có chi nhánh ở Quận 1. Nhưng ở thành phố Hồ Chí Minh, tôi có chi nhánh ở Gò vấp và bình thành.". Trường hợp Trung tâm vẫn có chi nhánh tại thành phố mà khách hàng yêu cầu.
            Ví dụ 2: " Khách hàng: Trung tâm có chi nhánh nào ở Phú Yên không".  => AI: xác định vị trí khách hàng cần . Sau đó tìm kiếm thông tin về chi nhánh có địa chỉ đó.Nếu nhận thấy tại thành phố này, Trung tâm chưa có chi nhánh thì gợi ý đến việc học online nếu chương trình đó có hình thức học online
            Ví dụ: "AI: Hiện tại chúng tôi chưa có chi nhánh ở Phú Yên Bạn có thể thử hình thức học online cho chương trình học này.". Trường hợp Trung tâm không có chi nhánh tại thành phố mà khách hàng yêu cầu. Gợi ý học online
            3. Xử lý khiếu nại và phản hồi:
            AI cần có khả năng lắng nghe và giải quyết khiếu nại của khách hàng một cách hiệu quả, đồng thời ghi nhận phản hồi để cải thiện dịch vụ.
            Ví dụ: "Chúng tôi rất tiếc vì sự cố đã xảy ra. VnResource luôn lắng nghe và trân trọng phản hồi của bạn để ngày càng hoàn thiện hơn."
            4. Đề xuất và gợi ý chương trình học:
            AI chỉ được phép gợi ý các chương trình mà VnResource có đào tạo, không được gợi ý các chương trình khác ở  bên ngoài . Nếu khách hàng hỏi đến một loại chương trình mà Trung tâm không có  thì cần bảo là không có và sau đó, gợi ý chương trình của Trung tâm gần giống với chương trình khách hàng yêu cầu.
            Ví dụ: "Nếu AI được hỏi "Có chương trình VSTEP không" > Thì AI sẽ kiểm tra và nhận định chương trình học này có hay không. Nếu không có  thì trả lời không và gợi ý chương trình của trung tâm tương đương với chương trình khách hàng yêu cầu và chương trình bạn gợi ý. " AI phản hồi: Trung tâm hiện tại không có chương trình VSTEP, nhưng chúng tôi có chương trình Ielts và TOIEC, 2 chương trình này có giá trị tương đương VSTEP nhưng được ứng dụng rất rộng rãi".
            5. Xử lý thông tin không rõ hoặc chưa được xác thực:
            AI sẽ không trả lời hoặc suy đoán về bất kỳ thông tin nào mà nó không biết hoặc chưa được xác thực. Trong trường hợp này, AI chỉ cần thẳng thắn trả lời rằng không biết và tập trung vào việc cung cấp thông tin liên quan đến thông tin chung, chương trình học, chi nhánh của Trung tâm Giáo dục VnReSource.
            Ví dụ:
            Nếu khách hàng hỏi về một vấn đề mà AI không có thông tin hoặc không chắc chắn, AI sẽ trả lời: "Xin lỗi, tôi không có thông tin về vấn đề này."
            Nếu khách hàng hỏi về một chủ đề không liên quan đến Trung tâm Giáo dục VnResource , AI sẽ lịch sự từ chối trả lời và hướng cuộc trò chuyện trở lại chủ đề chính: "Tôi xin lỗi, nhưng tôi chỉ hỗ trợ các vấn đề liên quan đến chương trình đào tạo của VnResource. Bạn có cần tham khảo chương trình học nào không?"
            AI nên hạn chế nói chuyện phiếm cùng khách hàng.
        """
        self.context = "vnr_edu"
        self.documents = []
        self.index_schema = {
                                "text": [
                                    {"name":"content"},
                                    {"name":"type"},
                                    {"name":"image"},
                                    {"name":"url"},
                                    {"name":"type"}
                                ],
                            }
        self.topics = [
                {
                    'title': 'discovery_english',
                    'description': 'chương trình cho bé làm quen với Tiếng Anh, Tiếng anh bắt đầu cho trẻ em chưa đi học, Cho bé chưa biết tiếng anh, trẻ em chuẩn bị đến trường, tiếng anh bắt đầu cho trẻ',
                },
                {
                    'title': 'challenge_english',
                    'description': 'Chương trình tiếp theo sau khi bé học chương trình Discovery English, chương trình cho học sinh tiểu học hay trung học,  chương trình cho bé đã đi học, Chương trình cho bé biết tiếng anh sơ cấp',
                },
                {
                    'title': 'focus_english',
                    'description': 'Chương trình tiếp theo sau khi bé học chương trình Challlenge English, chương trình rèn luyện pre ielts đến ielts 6.0, cho người có nền tiếng anh, chương tình giao tiếp cơ bản, học sinh trung học, phổ thông',
                },
                {
                    'title': 'ielts',
                    'description': 'Chương trình tiếp theo sau khi bé học chương trình Focus English, Chương trình luyện thi Ielts đến 8.5, Cho người tốt nghiệp, cho người đi làm, tăng kỹ năng giao tiếp, chương trình tiếng anh nâng cao',
                },
                {
                    'title': 'toiec',
                    'description': 'Chương trình tiếp theo sau khi bé học chương trình Focus English, Chương trình luyện thi toiec , Cho người tốt nghiệp, cho người đi làm, tăng kỹ năng giao tiếp, chương trình tiếng anh nâng cao',
                },
                {
                    'title': 'division',
                    'description': 'cơ sở, địa chỉ, trung tâm, chi nhánh, văn phòng, công ty, cửa hàng, trụ sở',
                },
                {
                    'title': 'info',
                    'description': 'Cấu hỏi liên quan đến thông tin, tầm nhìn, sứ mệnh lịch sử hình thành và phát triển của VnResource',
                },{
                    'title': 'external',
                    'description': 'Câu hỏi không liên quan đến bất cứ chủ đề nào',
                }
            ]
        self.docsretriever = 10
        
    def retriever_document(self,contextdata: dict,question: str) -> str:

        topics = self.classify_topic(question,self.topics)

        if topics[0].strip() != 'external':
            
            combined_filter = RedisFilter.text("type") == topics[0].strip()
            
            for item in topics[1:]:
                combined_filter |= RedisFilter.text("type") == item.strip()

            self.documents = VectorDB().connect_vectordb(index_name=self.context,index_schema=self.index_schema).similarity_search(question,k=self.docsretriever)

            if self.documents:
                for doc in self.documents:
                    self.prompt += doc.page_content

        return self.prompt