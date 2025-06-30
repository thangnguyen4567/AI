from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import HumanMessage, AIMessage
from factory.base.services import Services
from langchain_community.callbacks.manager import get_openai_callback


class Formula(Services):
    def __init__(self, config):

        super().__init__(config)
        self.enum = config.get("enum")

    def response(self):

        template = """
                Bạn là AI chuyên tạo công thức tính toán cho công ty theo yêu cầu của người dùng.
                Nhiệm vụ của bạn là tạo ra công thức tính toán phù hợp với ngữ cảnh.
                Công thức tính toán sẽ được sử dụng để tính toán kết quả của mục tiêu.
                Bản chỉ được trả lời công thức tính toán, KHÔNG CÓ GÌ KHÁC.
                VD trả về: [Tổng doanh số] / [Mục tiêu công ty] * 0.5 (chỉ được quyền sử dụng các enum trong danh sách enum) 
                Sử dụng các công thức và toán tử của excel để thiết lập (Ex: SUM(), IF(), .....) 
                Yêu cầu: {question}  
                Danh sách enum: {enum}
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
                "logic",
                "math",
                "datetime",
                "text",
                "operator",
                "check",
            ],
        )

        chain = prompt | self.model.llm

        with get_openai_callback() as cb:
            response = chain.invoke(
                {
                    "question": self.question,
                    "enum": self.enum,
                }
            )

        result = {"response": response.content}

        print(result)
        result["info"] = {
            "total_tokens": cb.total_tokens,
            "total_cost": cb.total_cost,
            "total_prompt_tokens": cb.prompt_tokens,
            "total_completion_tokens": cb.completion_tokens,
        }

        return result
