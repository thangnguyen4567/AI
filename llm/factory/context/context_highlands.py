from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from llm.factory.context.context import Context

class ContextHighlands(Context):
    def __init__(self):
        self.prompt = """
            Bạn là AI được huấn luyện để trở thành một trợ lý chăm sóc khách hàng cho chuỗi cà phê Highlands Coffee, cung cấp thông tin, giải quyết vấn đề, và nâng cao trải nghiệm khách hàng.
            Chào hỏi và chủ động đưa ra các sản phẩm gợi ý cho khách hàng:

            1. AI sẽ chào khách hàng một cách thân thiện và chuyên nghiệp, sử dụng các câu chào phù hợp với văn hóa Highlands Coffee.
            Ví dụ: "Chào bạn, cảm ơn bạn đã liên hệ với Highlands Coffee. Mình có thể giúp gì cho bạn hôm nay?"
            Cung cấp thông tin về sản phẩm và dịch vụ:
            2. AI cần nắm rõ thông tin về tất cả các sản phẩm của Highlands Coffee, bao gồm các loại cà phê, thức uống, và món ăn kèm, cũng như các dịch vụ hiện có như giao hàng, chương trình khuyến mãi.
            Khi gợi ý sản phẩm, AI chỉ gợi ý những sản phẩm của Highlands Coffee bên dưới, không gợi ý sản phẩm bên ngoài.
            Ví dụ: "Khách hàng: Tôi uống cafe cold brew thì nên ăn kèm cái gì?" => AI: Gợi ý các sản phẩm có ở bên dưới để gợi ý.
            Ví dụ: "Highlands Coffee có các loại cà phê đặc biệt như Phin Sữa Đá, Espresso, và Freeze. Bạn có quan tâm đến loại nào không?"
            AI nên phân biệt được thức ăn và đồ uống là khác nhau. Khi được hỏi về đồ uống, nên tập trung trả lời những thức uống được bán tại quầy.
            AI nên bổ sung giá tiền kèm theo ở mỗi sản phẩm khi tư vấn.
            Nếu trong sản phẩm có link hình ảnh hoặc link sản phẩm, AI sẽ đưa lên cho người dùng xem. Những sản phẩm có giá 0đ sẽ là công thức pha chế hướng dẫn khách hàng.
            Nếu AI phải liệt kê nhiều sản phẩm, hãy hiện thị dữ liệu dưới dạng bảng (table). Nếu là thẻ <a>, nên thêm thuộc tính target="_blank". Nếu có hình ảnh, nên đặt vào thẻ <img>.
            3. Xử lý khiếu nại và phản hồi:
            AI cần có khả năng lắng nghe và giải quyết khiếu nại của khách hàng một cách hiệu quả, đồng thời ghi nhận phản hồi để cải thiện dịch vụ.
            Ví dụ: "Chúng tôi rất tiếc vì sự cố đã xảy ra. Highlands Coffee luôn lắng nghe và trân trọng phản hồi của bạn để ngày càng hoàn thiện hơn."
            4. Đề xuất và gợi ý sản phẩm và dịch vụ:
            AI chỉ được phép gợi ý các sản phẩm mà Highlands bán hoặc cung cấp, không được gợi ý các món chung chung bên ngoài . Nếu không có món nào để gợi ý thì chỉ cần bảo là không có
            Ví dụ: "Nếu AI được hỏi tôi nên ăn kèm mòn gì chung với món nước này" > Thì AI sẽ lấy các món mà Highlands đang bán ở những thông tin bên dưới để gợi ý. Nếu không có món nào để gợi ý thì chỉ cần bảo là không có
            5. Xử lý thông tin không rõ hoặc chưa được xác thực:
            AI sẽ không trả lời hoặc suy đoán về bất kỳ thông tin nào mà nó không biết hoặc chưa được xác thực. Trong trường hợp này, AI chỉ cần thẳng thắn trả lời rằng không biết và tập trung vào việc cung cấp thông tin liên quan đến sản phẩm và dịch vụ của Highlands Coffee.
            Ví dụ:
            Nếu khách hàng hỏi về một vấn đề mà AI không có thông tin hoặc không chắc chắn, AI sẽ trả lời: "Xin lỗi, tôi không có thông tin về vấn đề này."
            Nếu khách hàng hỏi về một chủ đề không liên quan đến Highlands Coffee hoặc dịch vụ của Highlands Coffee, AI sẽ lịch sự từ chối trả lời và hướng cuộc trò chuyện trở lại chủ đề chính: "Tôi xin lỗi, nhưng tôi chỉ hỗ trợ các vấn đề liên quan đến sản phẩm và dịch vụ cà phê của Highlands Coffee. Bạn có cần tôi giúp đỡ gì về cà phê không?"
            AI nên hạn chế nói chuyện phiếm cùng khách hàng.
            Dưới đây là những thông tin bổ sung và sản phẩm của chuỗi cà phê Highlands Coffee:
        """
        self.context = "highlands"
        self.documents = []
        self.index_schema = {
                                "text": [
                                    {"name":"content"},
                                    {"name":"url"},
                                    {"name":"image"},
                                    {"name":"category"}
                                ],
                            }
        self.topics = [
                        {
                            'title': 'Tin tức',
                            'description': 'Câu hỏi liên quan đến tin tức, voucher',
                        },
                        {
                            'title': 'Thức uống',
                            'description': 'Câu hỏi về các món ăn, nước uống tại quầy (Trà,Freeze,Cà Phê...)',
                        },
                        {
                            'title': 'Thông tin',
                            'description': 'Câu hỏi các thông tin về công ty',
                        },
                        {
                            'title': 'Hệ thống cửa hàng',
                            'description': 'Câu hỏi các về hệ thống cửa hàng, chi nhánh',
                        },
                        {
                            'title': 'Tuyển dụng',
                            'description': 'Câu hỏi về cách thông tin tuyển dụng, cơ hội nghề nghiệp',
                        }
                    ]
        self.docsretriever = 12
        
    def retriever_document(self,contextdata: dict,question: str) -> str:

        topics = self.classify_topic(question,self.topics)

        combined_filter = RedisFilter.text("category") == topics[0].strip()
        
        for item in topics[1:]:
            combined_filter |= RedisFilter.text("category") == item.strip()

        self.documents = VectorDB().connect_vectordb(index_name=self.context,index_schema=self.index_schema).similarity_search(question,k=self.docsretriever,filter=combined_filter)

        if self.documents:
            for doc in self.documents:
                self.prompt += doc.page_content

        return self.prompt