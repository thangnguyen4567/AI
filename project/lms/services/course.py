from factory.base.services import Services
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from factory.base.services import Services
from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from typing import List
from tools.helper import file_reader
class Module(BaseModel):
    name: str = Field(description="Tên hoạt động hoặc tài nguyên trong lớp học")
    module: str = Field(description="Loại module: url (link đến video hoặc tài liệu), feedback (bài khảo sát, đánh giá lớp học hoặc giảng viên),quiz (bài kiểm tra, bài thi),resource (tài liệu),book (sách),assign (bài tập về nhà)")
    intro: str = Field(description="Giới thiệu về module này ở trong khóa học nhằm mục đích gì")

class Section(BaseModel):
    name: str = Field(description="Tên section trong khóa học")
    modules: List[Module]

class CourseInfo(BaseModel):
    fullname: str = Field(description="Tên khóa học")
    summary: str = Field(description="Giới thiệu tổng quan về khóa học, những kiến thức sẽ được tổ chức trong khóa theo từng section")
    sections: List[Section]
                                       
class Course(Services):
    def __init__(self,config):

        super().__init__(config)
        
        self.topic = config.get('topic')
        self.total_quiz = config.get('total_quiz')
        self.total_resource = config.get('total_resource')
        self.total_assign = config.get('total_assign')
        self.total_feedback = config.get('total_feedback')
        self.total_book = config.get('total_book')
        self.total_url = config.get('total_url')

    def response(self):

        resource = ''

        parser = JsonOutputParser(pydantic_object=CourseInfo)

        template = """
                Bạn là một AI chuyên tạo agenda 1 khóa học theo yêu cầu của người dùng.
                {format_instructions}
                Chủ đề: {topic}
                Sử dụng quiz khi cần tạo bài kiểm tra, bài thi cho khóa học
                Sử dụng feedback khi cần tạo bài khảo sát để hoặc viên vào đánh giá lớp học hoặc giảng viên 
                Sử dụng resource khi cần tạo tài liệu cho khóa học
                Sử dụng book khi cần tạo sách cho khóa học
                Sử dụng url khi cần tạo link hoặc video từ link tài liệu trích dẫn bên ngoài\
                Sử dụng assign khi cần tạo bài tập về nhà cho khóa học
                Yêu cầu: {question}
        """
        if self.total_quiz:
            template += "Số lượng quiz:"+str(self.total_quiz)
        if self.total_resource:
            template += "Số lượng resource:"+str(self.total_resource)
        if self.total_assign:
            template += "Số lượng bài tập:"+str(self.total_assign)
        if self.total_feedback:
            template += "Số lượng khảo sát:"+str(self.total_feedback)
        if self.total_book:
            template += "Số lượng sách:"+str(self.total_book)
        if self.total_url:
            template += "Số lượng video:"+str(self.total_url)
        if self.attachment_file:
            resource = file_reader(self.attachment_file)
            template += "Dựa trên nội dung sau:"+resource

        prompt = PromptTemplate(
            template=template,
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions(),"topic": self.topic},
        )

        chain = prompt | self.model.llm | parser

        response = chain.invoke({"question": self.question})
        
        return response