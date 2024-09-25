from factory.base.services import Services
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
import re
import json
from factory.base.services import Services
from pydantic import create_model

class CourseInfo(BaseModel):
    fullname: str = Field(description="Tên khóa học")
    summary: str = Field(description="Giới thiệu tổng quan về khóa học, những kiến thức sẽ được tổ chức trong khóa theo từng section")
    section: str = Field(description="Số lượng section")
    sectionname: list[str] = Field(description="Tên section tương ứng với số lượng (cách nhau bởi dấu chấm phẩy)")
    module: str = Field(description="Các loại tài nguyên được tổ chức trong bào gồm loại module như: quiz,feedback,resource,book,assignment (cách nhau bởi dấu chấm phẩy)")
    modulename: list[str] = Field(default_factory=list, description="Danh sách tên của các tài nguyên tương ứng với loại tài nguyên")
    
def create_dynamic_course_model(section_count: int):
    # Tạo dictionary chứa các field section động
    fields = {
        f'section{i+1}': (str, Field(description=f"Tên Section")) for i in range(section_count)
    }
    # Tạo model động kế thừa từ CourseInfo và thêm các section động
    DynamicCourseModel = create_model('DynamicCourseModel', __base__=CourseInfo, **fields)
    
    return DynamicCourseModel

# Ví dụ tạo model với 3 sections

class Course(Services):
    def __init__(self,config):

        super().__init__(config)

    def response(self):

        # DynamicModel = create_dynamic_course_model(3)
        parser = JsonOutputParser(pydantic_object=CourseInfo)
        # parser = JsonOutputParser(pydantic_object=DynamicModel)

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