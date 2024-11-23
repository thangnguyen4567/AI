from langchain.agents import tool
from config.config_vectordb import VectorDB
from langchain_core.runnables import RunnableConfig

@tool
def search_course(question: str, config: RunnableConfig) -> list:
    """ Tìm kiếm khóa học liên quan đến câu hỏi, tóm tắt khóa học..., khi cần gợi ý khóa học dựa vào câu hỏi của người dùng
        Đi kèm với các lệnh:Mở khóa học,mở lớp học

    Args:
        question: Câu hỏi người dùng về nhu cầu học tập, tóm tắt, gợi ý khóa học, kỹ năng cụ thể.
    """ 
    configuration = config.get("configurable", {})
    index_schema = {
        "text": [
            {"name":"source"},
            {"name":"title"},
            {"name":"content"},
        ],
        "numeric": [
            {"name":"courseid"},
        ]
    }
    prompt = ''
    try:
        document = VectorDB().connect_vectordb(index_name='course_'+configuration.get('dbname'), index_schema=index_schema).similarity_search(question, k=8)
        for doc in document:
            prompt += doc.page_content + ',link khóa học:' + doc.metadata['source'] + '--Hết thông tin khóa học--.\n'
    except:
        print('Chưa có dữ liệu training')

    return prompt