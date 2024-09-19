from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from factory.model_factory import ModelFactory
from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
import re
import json

class Question(BaseModel):
    qtype: str = Field(description="Loại câu hỏi")
    name: str = Field(description="Tên câu hỏi")
    questiontext: str = Field(description="Mô tả câu hỏi")
    answer1: str = Field(description="Đáp án 1")
    answer2: str = Field(description="Đáp án 2")
    answer3: str = Field(description="Đáp án 3")
    answer4: str = Field(description="Đáp án 4")
    defaultmark: str = Field(description="Điểm,luôn luôn bằng 1")
    result: str = Field(description="Đáp án đúng là 1 con số từ 1->4 ứng với answer")
    feedback: str = Field(description="Giải thích lý do chọn đáp án ở result")

class CreateQuestion():
    def __init__(self,config):

        self.question = config.get('question')
        self.qtype = config.get('qtype','multichoice')
        self.numberquestion = config.get('numberquestion','1')
        self.model = ModelFactory.create_model(self,config.get('model','chatgpt'))
        self.apikey = config.get('apikey')
        self.model.generate_model(self.apikey)
        self.project = config.get('project')
        self.coursemoduleid = config.get('coursemoduleid')

    def response(self):

        parser = JsonOutputParser(pydantic_object=Question)
        template = """
        Bạn là một AI tạo câu hỏi theo yêu cầu của người dùng. Dựa trên yêu cầu được cung cấp, bạn sẽ tạo ra một câu hỏi phù hợp với ngữ cảnh. 
        {format_instructions}
        Yêu cầu: {question} , Loại câu hỏi: {qtype}, số lượng câu hỏi: {numberquestion}, Câu hỏi được tạo dựa vào tài liệu: {resource}"""


        if self.coursemoduleid:
            index_schema = {
                "numeric": [
                    {"name":"coursemoduleid"},
                ]
            }
            filter = RedisFilter.num('coursemoduleid') == int(self.coursemoduleid)
            documents = VectorDB().connect_vectordb(index_name='course_'+self.project,index_schema=index_schema).similarity_search(self.question,k=8,filter=filter)
            resource = ''
            if documents:
                for doc in documents:
                    resource += doc.page_content
        else:
            resource = 'Chưa có tài liệu'


        prompt = PromptTemplate(
            template=template,
            input_variables=["question","qtype","numberquestion","resource"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model.llm

        response = chain.invoke({"question": self.question,
                                 "qtype": self.qtype,
                                 "numberquestion": self.numberquestion, 
                                 'resource': resource
                                 })
        
        cleaned_string = re.sub(r'```json|```','', response.content)

        json_blocks = re.findall(r'\{.*?\}', cleaned_string, re.DOTALL)

        json_objects = [json.loads(block) for block in json_blocks]

        return json_objects