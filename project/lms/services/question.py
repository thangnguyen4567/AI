from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from factory.model_factory import ModelFactory
from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
import re
import json

class QuestionMultichoice(BaseModel):
    qtype: str = Field(description="Loại câu hỏi chọn nhiều đáp án")
    name: str = Field(description="Tên câu hỏi")
    questiontext: str = Field(description="Mô tả câu hỏi")
    answer1: str = Field(description="Đáp án 1")
    answer2: str = Field(description="Đáp án 2")
    answer3: str = Field(description="Đáp án 3")
    answer4: str = Field(description="Đáp án 4")
    result: str = Field(description="Đáp án đúng là 1 con số từ 1->4 ứng với answer")
    generalfeedback: str = Field(description="Giải thích lý do chọn đáp án ở result")

class QuestionEssay(BaseModel):
    qtype: str = Field(description="Loại câu hỏi tự luận")
    name: str = Field(description="Tên câu hỏi")
    questiontext: str = Field(description="Mô tả câu hỏi tự luận")
    generalfeedback: str = Field(description="Giải thích cho câu hỏi tự luận")

class QuestionTrueFalse(BaseModel):
    qtype: str = Field(description="Loại câu hỏi đúng sai")
    name: str = Field(description="Tên câu hỏi")
    questiontext: str = Field(description="Mô tả câu hỏi tự luận")
    answer1: str = Field(description="Đáp án đúng")
    answer2: str = Field(description="Đáp án sai")
    result: str = Field(description="Đáp án đúng là 1:True hoặc 2:False")
    generalfeedback: str = Field(description="Giải thích cho câu hỏi")

class Question():
    def __init__(self,config):

        self.question = config.get('question')
        self.qtype = config.get('qtype','multichoice')
        self.numberquestion = config.get('numberquestion','1')
        self.model = ModelFactory.create_model(self,config.get('model','chatgpt'))
        self.apikey = config.get('apikey')
        self.model.generate_model(self.apikey)
        self.project = config.get('project')
        self.modules = config.get('coursemoduleid')
        self.chat_history = config.get('chat_history')

    def response(self):

        if self.qtype == 'multichoice':
            parser = JsonOutputParser(pydantic_object=QuestionMultichoice)
        elif self.qtype == 'essay':
            parser = JsonOutputParser(pydantic_object=QuestionEssay)
        elif self.qtype == 'truefalse':
            parser = JsonOutputParser(pydantic_object=QuestionTrueFalse)

        template = """
                Bạn là một AI chuyên tạo câu hỏi theo yêu cầu của người dùng. Nhiệm vụ của bạn là tạo ra **chính xác** {numberquestion} câu hỏi phù hợp với ngữ cảnh, không hơn không kém.
                {format_instructions}
                Yêu cầu: {question}  
                Loại câu hỏi: {qtype}  
                Câu hỏi phải dựa trên tài liệu sau: {resource} 
                
                **Lưu ý quan trọng:** Bạn phải tạo ra đúng {numberquestion} câu hỏi, và các câu hỏi phải tuân thủ loại yêu cầu ({qtype}). Không tạo thêm hoặc bớt câu hỏi.
        """

        if self.modules and self.modules[0]:
            
            combined_filter = RedisFilter.num('coursemoduleid') == int(self.modules[0])

            for item in self.modules[1:]:
                combined_filter = RedisFilter.num('coursemoduleid') == int(item)

            index_schema = {
                "numeric": [
                    {"name":"coursemoduleid"},
                ]
            }
            documents = VectorDB().connect_vectordb(index_name='resource_LMS_TEST_MISA',index_schema=index_schema).similarity_search(self.question,k=8,filter=combined_filter)
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