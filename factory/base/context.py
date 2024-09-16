from abc import ABC, abstractmethod 
from tools.helper import remove_stopwords
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

class Context(ABC):
    def __init__(self):
        pass

    ##Lấy danh sách document theo context
    @abstractmethod
    def retriever_document(self,contextdata: dict,question: str) -> str:
        pass

    ##Tổng hợp lại câu hỏi > để ko bị miss context cũ đối với những câu hỏi follow-up
    def aggregation_question_context(self,chat_history: list,question) -> str:
        
        aggregation = ''

        if chat_history is not None:
            for chat in chat_history[-3:]:
                if 'human' in chat:
                    aggregation += ' '+chat['human']

        aggregation += ' '+question

        return aggregation

    ##Phân loại câu hỏi theo chủ đề
    def classify_topic(self,question,topics) -> list:
        
        apikey = os.getenv("OPENAI_API_KEY")
        topic = ''
        for item in topics:
            topic += item['title']+':'+item['description']+'\n'

        template = """
            Bạn là một AI phân loại câu hỏi của người dùng vào các chủ đề cụ thể. Dựa trên nội dung câu hỏi, xác định tất cả các chủ đề phù hợp nhất từ danh sách sau:
            {topic}
            Phân tích câu hỏi của người dùng và trả về **danh sách tên các chủ đề** phù hợp nhất từ danh sách trên mà không kèm thêm bất kỳ từ nào khác. Nếu câu hỏi liên quan đến nhiều chủ đề, hãy trả về tất cả các chủ đề đó.
            Câu hỏi của người dùng: "{question}"
            Định dạng đầu ra: Tên Chủ đề 1, Tên Chủ đề 2,...
        """

        prompt = PromptTemplate(
            input_variables=["topic","question"],
            template=template
        )

        llm = ChatOpenAI(model="gpt-4o-mini",api_key=apikey,temperature=0)

        chain = prompt | llm

        response = chain.invoke({
            "topic": topic,
            "question": question
        })
        listtopic = response.content.split(',')
        return listtopic
