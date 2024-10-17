from factory.base.services import Services
from langchain.prompts import PromptTemplate
from factory.base.services import Services
from config.config_vectordb import VectorDB
from langchain_community.vectorstores.redis import RedisFilter
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from typing import List

class AssignmentInfo(BaseModel):
    question: List[str] = Field(description="Câu hỏi bài tập về nhà")

class Assignment(Services):
    def __init__(self,config):

        super().__init__(config)

        self.coursemoduleids = config.get('coursemoduleids')

    def response(self):

        resource = ''

        if self.coursemoduleids and self.coursemoduleids[0]:
            
            combined_filter = RedisFilter.num('coursemoduleids') == int(self.coursemoduleids[0])

            for item in self.coursemoduleids[1:]:
                combined_filter |= RedisFilter.num('coursemoduleids') == int(item)

            index_schema = {
                "numeric": [
                    {"name":"coursemoduleids"},
                ]
            }
            documents = VectorDB().connect_vectordb(index_name='resource_'+self.contextdata['collection'],index_schema=index_schema).similarity_search(self.question,k=8,filter=combined_filter)
            if documents:
                for doc in documents:
                    resource += doc.page_content

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

        response = chain.invoke({"question": self.question,"resource":resource})
        
        return response