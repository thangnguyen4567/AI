from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from factory.base.services import Services
from langchain_community.callbacks.manager import get_openai_callback
from tools.helper import file_reader

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
    qtype: str = Field(description="Loại câu hỏi tự luận, mỗi câu hỏi tự luận sẽ có qtype,name,questiontext,generalfeedback được tách ra riêng biệt")
    name: str = Field(description="Tên câu hỏi")
    questiontext: str = Field(description="Đề bài cho 1 câu hỏi tự luận")
    generalfeedback: str = Field(description="Giải thích cho câu hỏi tự luận")

class QuestionTrueFalse(BaseModel):
    qtype: str = Field(description="Loại câu hỏi đúng sai")
    name: str = Field(description="Tên câu hỏi")
    questiontext: str = Field(description="Mô tả câu hỏi tự luận")
    answer1: str = Field(description="Đáp án đúng")
    answer2: str = Field(description="Đáp án sai")
    result: str = Field(description="Đáp án đúng là 1:True hoặc 2:False")
    generalfeedback: str = Field(description="Giải thích cho câu hỏi")

class Question(Services):
    def __init__(self,config):

        super().__init__(config)

        self.qtype = config.get('qtype','multichoice')
        self.numberquestion = config.get('numberquestion')
        self.modules = config.get('coursemoduleid')
        self.collection = 'resource_'+self.contextdata['collection']

    def response(self):

        if self.qtype == 'multichoice':
            parser = JsonOutputParser(pydantic_object=QuestionMultichoice)
        elif self.qtype == 'essay':
            parser = JsonOutputParser(pydantic_object=QuestionEssay)
        elif self.qtype == 'truefalse':
            parser = JsonOutputParser(pydantic_object=QuestionTrueFalse)

        template = """
                Bạn là một AI chuyên tạo câu hỏi theo yêu cầu của người dùng. Nhiệm vụ của bạn là tạo ra **chính xác** {numberquestion} câu hỏi phù hợp với ngữ cảnh, không hơn không kém.
                Mỗi câu hỏi được tạo ra sẽ đi theo cấu trúc json dưới đây:
                {format_instructions}
                Yêu cầu: {question}  
                Loại câu hỏi: {qtype}  
                Câu hỏi phải dựa trên tài liệu sau: {resource} 
                **Lưu ý quan trọng:** Bạn phải tạo ra đúng số lượng {numberquestion} câu hỏi, và các câu hỏi phải tuân thủ loại yêu cầu ({qtype}). Không tạo thêm hoặc bớt câu hỏi.
        """
        try:
            if self.modules and self.modules[0]:
                    
                combined_filter = RedisFilter.num('coursemoduleid') == int(self.modules[0])

                for item in self.modules[1:]:
                    combined_filter |= RedisFilter.num('coursemoduleid') == int(item)

                index_schema = {
                    "numeric": [
                        {"name":"coursemoduleid"},
                    ]
                }
                documents = VectorDB().connect_vectordb(index_name=self.collection,index_schema=index_schema).similarity_search(self.question,k=8,filter=combined_filter)
                resource = ''
                if documents:
                    for doc in documents:
                        resource += doc.page_content
            else:
                resource = 'Chưa có tài liệu'
        except Exception as e:
            resource = 'Chưa có tài liệu'
            print(e)
            
        if self.attachment_file:
            resource = file_reader(self.attachment_file)

        prompt = PromptTemplate(
            template=template,
            input_variables=["question","qtype","numberquestion","resource"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model.llm | parser

        with get_openai_callback() as cb:
            response = chain.invoke({"question": self.question,
                                "qtype": self.qtype,
                                "numberquestion": self.numberquestion, 
                                'resource': resource
                                })

        result = {}
        if 'foo' in response:
            result['response'] = response['foo']
        elif 'questions' in response:
            result['response'] = response['questions']
        elif self.qtype == 'essay':
            result['response'] = [response]
        elif self.numberquestion == '1':
            result['response'] = [response]
        else:
            result['response'] = response

        result['info'] = {
            'total_tokens': cb.total_tokens,
            'total_cost': cb.total_cost,
            'total_prompt_tokens': cb.prompt_tokens,
            'total_completion_tokens': cb.completion_tokens
        }

        return result