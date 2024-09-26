from factory.base.services import Services
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from factory.base.services import Services

class CourseInfo(BaseModel):
    fullname: str = Field(description="Tên khóa học")
    summary: str = Field(description="Giới thiệu tổng quan về khóa học, những kiến thức sẽ được tổ chức trong khóa theo từng section")
    section: str = Field(description="Số lượng section")
    sectionname: list[str] = Field(description="Tên section tương ứng với số lượng")
    module: str = Field(description="Các loại tài nguyên được tổ chức trong bào gồm loại module như: quiz,feedback,resource,book,assignment")
    modulename: list[str] = Field(description="Danh sách tên của các tài nguyên tương ứng với loại tài nguyên")
    
class Course(Services):
    def __init__(self,config):

        super().__init__(config)

    def response(self):

        parser = JsonOutputParser(pydantic_object=CourseInfo)

        template = """
                Bạn là một AI chuyên tạo agenda 1 khóa học theo yêu cầu của người dùng.
                {format_instructions}
                Yêu cầu: {question}  
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model.llm | parser

        response = chain.invoke({"question": self.question})
        
        return response