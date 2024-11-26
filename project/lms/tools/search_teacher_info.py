from langchain.agents import tool
import requests
from langchain_core.runnables import RunnableConfig

@tool
def search_teacher_info(courseids: list, config: RunnableConfig) -> list:
    """ Tìm kiếm danh sách khóa học đang giảng dạy của giáo viên, tiến độ học tập của học viên trong các khóa học đó""" 

    configuration = config.get("configurable", {})
    token = configuration.get('token')
    endpoint = configuration.get('endpoint')
    data = {
        "courseids": courseids,
        "userid": configuration.get('userid'),
    }
    headers = {
        "Accept-Charset": "",
        "Content-Type": "application/json",
        "Authorization": "Bearer "+token,
    }

    url = endpoint+"/api/integrated/ai/teacher-course"
    try:
        response = requests.get(url, json=data, headers=headers)
        return str(response.json()['data'])
    except requests.exceptions.RequestException as e:
        return 'Không tìm thấy dữ liệu'