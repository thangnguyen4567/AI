from langchain.agents import tool
import requests
from langchain_core.runnables import RunnableConfig

@tool
def search_student_course(time: str, config: RunnableConfig) -> list:
    """ Tìm kiếm dánh sách khóa học đã được ghi danh của học viên, 
        Tìm kiếm dánh sách module mà học viên đang học, các tài nguyên mà học viên đã,đang học. tiến trình học tập của học viên, đã học xong hay chưa học xong cái gì """ 
    
    configuration = config.get("configurable", {})
    data = {
        "userid": configuration.get('userid'),
        # "time": int(time.timestamp())
    }
    token = configuration.get('token')
    endpoint = configuration.get('endpoint')
    headers = {
        "Accept-Charset": "",
        "Content-Type": "application/json",
        "Authorization": "Bearer "+token,
    }

    url = endpoint+"/api/integrated/ai/student-courses"
    try:
        response = requests.get(url, json=data, headers=headers)
        return str(response.json()['data'])
    except requests.exceptions.RequestException as e:
        return 'Không tìm thấy khóa học'