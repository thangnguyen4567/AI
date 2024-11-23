from langchain.agents import tool
from langchain_community.vectorstores.redis import RedisFilter
from config.config_vectordb import VectorDB
from langchain_core.runnables import RunnableConfig

@tool
def search_hdsd(role: str,question: str, config: RunnableConfig) -> list:
    """ - Câu hỏi về hướng dẫn vai trò học viên các chức năng: Đăng nhập, Dashboard học viên, 
        xem lịch, tham gia lớp học, hướng dẫn các hoạt động trong lớp, 
        làm khảo sát và kì thi, tra cứu thư viện, diễn đàn, tin tức
        - Câu hỏi về hướng dẫn vai trò quản lý đào tạo các chức năng: Chuyển đổi vai trò hệ thống, Dashboard QLĐT, 
        Các chức năng quản lý, Import dữ liệu, quản lý các màn hình báo cáo, 
        tạo câu hỏi, tạo khóa học, Xây dựng nội dung và hoạt động trong lớp học, 
        Quản lý năng lực và lộ trình đào tạo, M point, quản lý kì thi, 
        tin tức, thư viện, ngân hàng câu hỏi
        - Câu hỏi về hướng dẫn sử dụng vai trò giáo viên,giảng viên các chức năng: Xây dựng nội dung hoạt động trong lớp, 
        Thiết lập điểm, Chấm điểm, Nhận xét học viên, Dashboard giảng viên, 
        Phê duyệt, đánh giá
    Args:
        role: student hoặc manager hoặc teacher
        question: câu hỏi cần trả lời
    """
    
    index_schema = {
        "text": [
            {"name":"title"},
            {"name":"role"},
            {"name":"content"},
            {"name":"source"}
        ],
    }
    filter = RedisFilter.text("role") == role
    prompt = ''
    try:
        document = VectorDB().connect_vectordb(index_name='hdsd', index_schema=index_schema).similarity_search(question, k=5, filter=filter)
        for doc in document:
            prompt += doc.page_content + ', link tài liệu hdsd: ['+doc.metadata['title']+']' + doc.metadata['source'] + '.\n'
    except:
        print('Chưa có dữ liệu training')

    return prompt