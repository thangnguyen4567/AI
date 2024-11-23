from langchain.agents import tool
import requests
from langchain_core.runnables import RunnableConfig

@tool
def search_student_module(time: str, courseids: list, config: RunnableConfig) -> list:
    """ Tìm kiếm dánh sách module mà học viên đang học, các tài nguyên mà học viên đã,đang học. tiến trình học tập của học viên """ 

    configuration = config.get("configurable", {})
    token = configuration.get('token')
    endpoint = configuration.get('endpoint')
    data = {
        "courseids": courseids,
        "userid": configuration.get('userid'),
        "time": int(time.timestamp())
    }
    headers = {
        "Accept-Charset": "",
        "Content-Type": "application/json",
        "Authorization": "Bearer "+token,
    }

    url = endpoint+"/api/integrated/ai/student-modules"
    try:
        response = requests.get(url, json=data, headers=headers)
        return str(response.json()['data'])
    except requests.exceptions.RequestException as e:
        return 'Không tìm thấy dữ liệu'