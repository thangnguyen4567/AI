from factory.base.services import Services
from langchain.prompts import PromptTemplate
from factory.base.services import Services
from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from typing import List
from langchain_community.callbacks.manager import get_openai_callback

class AssignmentInfo(BaseModel):
    question: List[str] = Field(description="Câu hỏi bài tập về nhà")

class Assignment(Services):
    def __init__(self,config):

        super().__init__(config)

        self.coursemoduleids = config.get('coursemoduleids')
        self.collection = 'resource_'+self.contextdata['collection']

    def response(self):

        resource = ''

        try:
            if self.coursemoduleids and self.coursemoduleids[0]:
                
                combined_filter = RedisFilter.num('coursemoduleid') == int(self.coursemoduleids[0])

                for item in self.coursemoduleids[1:]:
                    combined_filter |= RedisFilter.num('coursemoduleid') == int(item)

                index_schema = {
                    "numeric": [
                        {"name":"coursemoduleid"},
                    ]
                }
                documents = VectorDB().connect_vectordb(index_name=self.collection,index_schema=index_schema).similarity_search(self.question,k=8,filter=combined_filter)
                if documents:
                    for doc in documents:
                        resource += doc.page_content
        except Exception as e:
            print(e)

        if resource:
            resource = 'Dựa trên nội dung sau:'+str(resource)
        else:
            resource = 'Chưa có tài liệu'

        template = """
                Bạn là một AI chuyên tạo gia tạo câu hỏi cho bài tập về nhà.
                {format_instructions}
                Yêu cầu: {question}
                Tài liệu: {resource}
        """

        parser = JsonOutputParser(pydantic_object=AssignmentInfo)

        prompt = PromptTemplate(
            template=template,
            input_variables=["question","resource"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model.llm | parser

        with get_openai_callback() as cb:
            response = chain.invoke({"question": self.question,"resource":resource})
        
        result = {}
        result['response'] = response
        result['info'] = {
            'total_tokens': cb.total_tokens,
            'total_cost': cb.total_cost,
            'total_prompt_tokens': cb.prompt_tokens,
            'total_completion_tokens': cb.completion_tokens
        }

        return result