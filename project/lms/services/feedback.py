from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from factory.base.services import Services
from langchain_community.callbacks.manager import get_openai_callback
from tools.helper import file_reader

class QuestionMultichoice(BaseModel):
    name: str = Field(description="Tên câu hỏi")
    answer1: str = Field(description="Đáp án 1")
    answer2: str = Field(description="Đáp án 2")
    answer3: str = Field(description="Đáp án 3")
    answer4: str = Field(description="Đáp án 4")

class Feedback(Services):
    def __init__(self,config):

        super().__init__(config)

        self.collection = 'resource_'+self.contextdata['collection']

    def response(self):

        parser = JsonOutputParser(pydantic_object=QuestionMultichoice)
        template = """
                Bạn là một AI chuyên tạo câu hỏi theo yêu cầu của người dùng. Nhiệm vụ của bạn là tạo ra câu hỏi khảo sát trong khóa học phù hợp với ngữ cảnh.
                Mỗi câu hỏi được tạo ra sẽ đi theo cấu trúc json dưới đây:
                {format_instructions}
                Yêu cầu: {question}  
                Câu hỏi phải dựa trên tài liệu sau: {resource} 
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
            input_variables=["question","resource"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model.llm | parser

        with get_openai_callback() as cb:
            response = chain.invoke({"question": self.question,'resource': resource})

        result = {}
        # Kiểm tra xem response có phải là list hay không
        if isinstance(response, list):
            result['response'] = response
        else:
            result['response'] = [response]  # Chuyển đổi thành list nếu không phải

        result['info'] = {
            'total_tokens': cb.total_tokens,
            'total_cost': cb.total_cost,
            'total_prompt_tokens': cb.prompt_tokens,
            'total_completion_tokens': cb.completion_tokens
        }

        return result