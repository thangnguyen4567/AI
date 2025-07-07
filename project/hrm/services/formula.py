from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import HumanMessage, AIMessage
from factory.base.services import Services
from langchain_community.callbacks.manager import get_openai_callback
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


class FormulaDetail(BaseModel):
    formula: str = Field(
        description="""
        VD: [Tổng doanh số] / [Mục tiêu công ty] * 0.5 (chỉ được quyền sử dụng các enum trong danh sách enum) 
        Sử dụng các công thức và toán tử của excel để thiết lập (Ex: SUM(), IF(), .....) 
        """
    )
    description: str = Field(description="Giải thích công thức")


class Formula(Services):
    def __init__(self, config):

        super().__init__(config)
        self.enum = config.get("enum")
        self.prompt = config.get("prompt")

    def response(self):

        parser = JsonOutputParser(pydantic_object=FormulaDetail)

        template = """
        Bạn là một AI chuyên tạo công thức kế toán/phân bổ trong dạng biểu thức (formula). 
        Không được tính kết quả, chỉ tạo công thức với các biến dưới dạng enum.
        Bạn là chuyên viên hoạch định chiến lược với hơn 15 năm kinh nghiệm cho doanh nghiệp phần mềm, có tầm nhìn và sứ mệnh xây dựng tập đoàn phần mềm nhân sự hàng đầu Việt Nam.
        Tôi đang cần bạn thực hiện phân bổ một mục tiêu đo lường được (ví dụ: doanh thu, lợi nhuận, chi phí, số lượng khách hàng...) theo thời gian (4 quý hoặc 12 tháng) trong năm.
        Mục tiêu cần phân bổ là: Tổng doanh thu toàn tập đoàn năm 2025 với chỉ tiêu đạt 120.000 tỷ VNĐ.
        Yêu cầu phân bổ phải dựa trên các yếu tố có thực trong ngành phần mềm nhân sự tại Việt Nam, bao gồm:
        Chu kỳ kinh doanh của ngành phần mềm B2B tại Việt Nam
        Biến động nhân sự và hành vi ra quyết định của khách hàng theo từng quý
        Tác động của mùa vụ (ví dụ: Tết, thời điểm duyệt ngân sách, mùa tuyển dụng)
        Đặc điểm địa phương (Bắc – Trung – Nam) nếu cần
        Sau khi phân tích và phân bổ phù hợp cho 4 quý trong năm, hãy xuất ra công thức Excel theo đúng cú pháp sau:
        =IF(Quy=1, Muc_Tieu*X%, IF(Quy=2, Muc_Tieu*Y%, IF(Quy=3, Muc_Tieu*Z%, IF(Quy=4, Muc_Tieu*W%, 0))))
        Trong đó:
        Muc_Tieu là ô chứa tổng mục tiêu (ví dụ: 120000)
        Quy là ô chứa số quý (1 đến 4)
        Các tỷ lệ phần trăm (X, Y, Z, W) là trọng số phân bổ theo quý sau khi đã tính toán theo nghiệp vụ
        Chỉ cần trả lại duy nhất công thức Excel, không cần giải thích thêm.
        Chỉ tạo công thức (không được gán giá trị cụ thể).
        Ngữ cảnh: {prompt} với yêu cầu: {question} 
        Danh sách enum: {enum} (chỉ được sử dụng các enum trong danh sách enum này không được chế thêm)
        Công thức được tạo ra sẽ đi theo cấu trúc json dưới đây ( bắt buộc chỉ trả lời json , không có gì khác, nếu không sẽ bị lỗi):
        {format_instructions}
        Lưu ý: Không được dùng hàm : COUNTA(), chỉ trả về công thức tính toán, không có gì khác.

        """

        message = [SystemMessagePromptTemplate.from_template(template)]

        if self.chat_history is not None:
            for chat in self.chat_history:
                if "human" in chat:
                    message.append(HumanMessage(content=chat["human"]))
                if "bot" in chat and chat["bot"] != None:
                    message.append(AIMessage(content=chat["bot"]))
            message.append(HumanMessagePromptTemplate.from_template("{question}"))

        prompt = ChatPromptTemplate(
            messages=message,
            input_variables=[
                "question",
                "enum",
                "prompt",
            ],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model.llm | parser

        with get_openai_callback() as cb:
            response = chain.invoke(
                {
                    "question": self.question,
                    "enum": self.enum,
                    "prompt": self.prompt,
                }
            )

        result = {}
        if "properties" in response:
            result["response"] = response["properties"]
        else:
            result["response"] = response

        result["info"] = {
            "total_tokens": cb.total_tokens,
            "total_cost": cb.total_cost,
            "total_prompt_tokens": cb.prompt_tokens,
            "total_completion_tokens": cb.completion_tokens,
        }

        return result
