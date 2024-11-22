from langchain.agents import tool
from config.config_vectordb import VectorDB

@tool
def search_resource(question: str,dbname: str) -> list:
    """ Tìm kiếm thông tin
        Tìm kiếm tài liệu để trả lời cho câu hỏi của người dùng mà AI không có thông tin liên quan
        Tìm kiếm tài liệu liên quan đến câu hỏi,tóm tắt tài liệu nằm trong lớp học,khóa học,khi cần gợi ý tài liệu dựa vào câu hỏi của người dùng
        Đi kèm với các lệnh:đọc tài liệu,mở tài liệu
    Args:
        question: Câu hỏi người dùng về nhu cầu học tập, tóm tắt, gợi ý tài liệu dựa vào câu hỏi của người dùng
    """ 
    index_schema = {
        "text": [
            {"name":"source"},
            {"name":"title"},
            {"name":"content"},
        ],
        "numeric": [
            {"name":"courseid"},
            {"name":"coursemoduleid"},
        ]
    }
    prompt = ''
    try:
        document = VectorDB().connect_vectordb(index_name='resource_'+dbname, index_schema=index_schema).similarity_search(question, k=8)    
        for doc in document:
            prompt += doc.page_content + ',nguồn '+ doc.metadata['title'] + ':' + doc.metadata['source'] + '.\n'
    except:
        print('Chưa có dữ liệu training')

    return prompt