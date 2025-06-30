from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from factory.base.services import Services
from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.output_parsers import JsonOutputParser


class GoalDetail(BaseModel):
    ID: int = Field(description="ID mục tiêu")
    GoalName: str = Field(description="Tên mục tiêu")
    Department: str = Field(description="Phòng ban")
    TotalTarget: int = Field(description="Tổng mục tiêu")
    Unit: str = Field(
        description="Đơn vị ('currency' : tiền, 'percent' : phần trăm, 'number' : số lượng)"
    )
    ParentID: int = Field(description="ID mục tiêu cha nếu ko có thì mặc định null")
    HasChildren: bool = Field(description="Có con không nếu ko có thì mặc định false")
    Weight: str = Field(
        description="Trọng số mục tiêu tổng Tổng trọng số mục tiêu tổng là 100%"
    )
    Type: str = Field(
        description="Loại mục tiêu 'Tài chính', 'Khách hàng', 'Nội bộ', 'Sản phẩm', 'Quy trình', 'Khác', 'Đào tạo & Phát triển'"
    )
    Guideline: str = Field(description="Hướng dẫn thực hiện mục tiêu")


class Goal(Services):
    def __init__(self, config):

        super().__init__(config)

    def response(self):

        parser = JsonOutputParser(pydantic_object=GoalDetail)

        template = """
                Bạn là một AI chuyên tạo Nhiều mục tiêu cho công ty theo yêu cầu của người dùng. Nhiệm vụ của bạn là tạo ra mục tiêu phù hợp với ngữ cảnh. Đôi khi mục tiêu cha 
                sẽ có mục tiêu con , mỗi phòng ban tạo ít nhất 8 mục tiêu cha, sl mục tiêu con phụ thuộc vào mục tiêu cha ,
                bạn sẽ chia mục tiêu theo 2 loại mục tiêu chuẩn là OKR và KPI tùy vào yêu cầu
                Mỗi mục tiêu được tạo ra sẽ đi theo cấu trúc json dưới đây ( bắt buộc chỉ trả lời json , không có gì khác, nếu không sẽ bị lỗi):
                {format_instructions}
                Yêu cầu: {question}  
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model.llm | parser

        with get_openai_callback() as cb:
            response = chain.invoke({"question": self.question})

        result = {}
        if "properties" in response:
            result["response"] = response["properties"]
        else:
            result["response"] = response

        print(result)
        result["info"] = {
            "total_tokens": cb.total_tokens,
            "total_cost": cb.total_cost,
            "total_prompt_tokens": cb.prompt_tokens,
            "total_completion_tokens": cb.completion_tokens,
        }

        return result
