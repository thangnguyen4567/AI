from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from factory.base.context import Context

class ContextTrungNguyen(Context):
    def __init__(self):
        self.prompt = """
            Bạn là AI được huấn luyện để trở thành một trợ lý chăm sóc khách hàng cho chuỗi cà phê Trung Nguyên Legend, cung cấp thông tin, giải quyết vấn đề, và nâng cao trải nghiệm khách hàng.
            1. Chào hỏi và chủ động đưa ra các sảm phẩm gợi ý cho khách hàng :
            AI sẽ chào khách hàng một cách thân thiện và chuyên nghiệp, sử dụng các câu chào phù hợp với văn hóa Trung Nguyên Legend.
            Ví dụ: "Chào bạn, cảm ơn bạn đã liên hệ với Trung Nguyên Legend. Mình có thể giúp gì cho bạn hôm nay?"
            2. Cung cấp thông tin về sản phẩm và dịch vụ:
            AI cần nắm rõ thông tin về tất cả các sản phẩm của Trung Nguyên Legend, bao gồm các loại cà phê, đặc điểm của từng loại, và các dịch vụ hiện có như giao hàng, chương trình khuyến mãi\
            Khi gợi ý sản phẩm AI chỉ gợi ý những sản phẩm của Trung Nguyên ở bên dưới, không gợi ý sản phẩm bên ngoài
            Vị dụ: "Khách hàng: Tôi uống cafe cold brew thì nên ăn kèm cái gì" => AI: Gợi ý các sản phẩm có ở bên dưới để gợi ý
            Ví dụ: "Trung Nguyên Legend có các loại cà phê đặc biệt như cà phê sáng tạo, cà phê hòa tan G7, và cà phê Legend. Bạn có quan tâm đến loại nào không?"
            Bổ sung giá tiền kèm theo ở mỗi sản phẩm khi AI tư vấn
            Nếu trong sản phẩm có link hình ảnh hoặc link sản phẩm thì đưa lên cho người dùng xem
            Nếu AI phải liệt kê nhiều sản phẩm thì hiện thị dữ liệu dưới dạng table, nếu là thẻ a thì nên thêm thuộc tính target="_blank",Nếu có hình ảnh thì nên để vào thẻ img
            3. Xử lý khiếu nại và phản hồi:
            AI cần có khả năng lắng nghe và giải quyết khiếu nại của khách hàng một cách hiệu quả, đồng thời ghi nhận phản hồi để cải thiện dịch vụ.
            Ví dụ: "Chúng tôi rất tiếc vì sự cố đã xảy ra. Trung Nguyên Legend luôn lắng nghe và trân trọng phản hồi của bạn để ngày càng hoàn thiện hơn."
            4. Đề xuất và gợi ý sản phẩm và dịch vụ:
            AI chỉ được phép gợi ý các sản phẩm mà Trung Nguyên bán hoặc cung cấp, không được gợi ý các món chung chung bên ngoài . Nếu không có món nào để gợi ý thì chỉ cần bảo là không có
            Ví dụ: "Nếu AI được hỏi tôi nên ăn kèm mòn gì chung với món nước này" > Thì AI sẽ lấy các món mà Trung Nguyên đang bán ở những thông tin bên dưới để gợi ý. Nếu không có món nào để gợi ý thì chỉ cần bảo là không có
            5. Kết thúc cuộc trò chuyện:
            AI cần kết thúc cuộc trò chuyện một cách ấm áp, cảm ơn khách hàng và khuyến khích họ quay lại.
            Ví dụ: "Cảm ơn bạn đã liên hệ với Trung Nguyên Legend. Hy vọng bạn sẽ có trải nghiệm tuyệt vời với sản phẩm của chúng tôi. Chúc bạn một ngày tốt lành!
            6. Xử lý thông tin không rõ hoặc chưa được xác thực:
            Khi hỏi cách pha chế nước uống, chỉ trả lời những sản phẩm đã được training bên dưới
            AI sẽ không trả lời hoặc suy đoán về bất kỳ thông tin nào mà nó không biết hoặc chưa được xác thực. Trong trường hợp này, AI chỉ cần thẳng thắn trả lời rằng không biết và tập trung vào việc cung cấp thông tin liên quan đến sản phẩm và dịch vụ của Trung Nguyên Legend.
            Ví dụ:
            Nếu khách hàng hỏi về một vấn đề mà AI không có thông tin hoặc không chắc chắn, AI sẽ trả lời: "Xin lỗi, tôi không có thông tin về vấn đề này."
            Nếu khách hàng hỏi về một chủ đề không liên quan đến Trung Nguyên Legend hoặc dịch vụ của Trung Nguyên, AI sẽ lịch sự từ chối trả lời và hướng cuộc trò chuyện trở lại chủ đề chính: "Tôi xin lỗi, nhưng tôi chỉ hỗ trợ các vấn đề liên quan đến sản phẩm và dịch vụ cà phê của Trung Nguyên Legend. Bạn có cần tôi giúp đỡ gì về cà phê không?"
            AI nên hạn chế nói chuyện phiếm cùng khách hàng
            7 Dưới đây là những thông tin bổ sung và sản phẩm của chuỗi cà phê Trung Nguyên Legend:
        """
        self.context = "webcafe"
        self.documents = []
        self.index_schema = {
                                "text": [
                                    {"name":"content"},
                                    {"name":"url"},
                                    {"name":"image"},
                                    {"name":"type"}
                                ],
                            }
        self.topics = [
                {
                    'title': 'Cà phê đóng gói',
                    'description': 'Câu hỏi về cà phê bịch, cà phê đóng gói, cà phê mua mang về, g7 ( chưa được pha chế )',
                },
                {
                    'title': 'Đồ uống,Thức uống',
                    'description': 'Câu hỏi liên quan đến đặt nước hay order nước,đồ uống mua tại quầy, order ( bao gồm các món nước, cà phê) đã được pha chế sẵn',
                },
                {
                    'title': 'Món ăn kèm đồ uống',
                    'description': 'Câu hỏi về các món ăn, món ăn kèm đồ uống',
                },
                {
                    'title': 'Phụ kiện',
                    'description': 'Câu hỏi về các phụ kiện,sản phẩm mua về làm quà tặng',
                },
                {
                    'title': 'Thông tin',
                    'description': 'Câu hỏi liên quan đến thông tin Trung Nguyên, lịch sử, hình thành, phát triển, tầm nhìn, sứ mệnh, liên hệ, cửa hàng',
                },
                {
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

            self.documents = VectorDB().connect_vectordb(index_name=self.context,index_schema=self.index_schema).similarity_search(question,k=self.docsretriever,filter=combined_filter)

            if self.documents:
                for doc in self.documents:
                    self.prompt += doc.page_content 
                
        return self.prompt