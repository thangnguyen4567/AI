from langchain.agents import tool
import requests
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    startdate: str = Field(description="Thời gian bắt đầu")
    enddate: str = Field(description="Thời gian kết thúc")
    coursename: str = Field(description="Tên khóa học (ko bắt buộc)")

@tool("search_student_course", args_schema=SearchInput, return_direct=True)
def search_student_course(startdate : datetime, enddate: datetime, coursename: str, config: RunnableConfig) -> list:
    """ Tìm kiếm dánh sách khóa học đã được ghi danh của học viên,
        Tìm kiếm dánh sách module mà học viên đang học, các tài nguyên mà học viên đã,đang học. tiến trình học tập của học viên, đã học xong hay chưa học xong cái gì 
    """ 
    # Thời gian tìm kiếm từ startdate đến enddate bắt buộc phải có, nếu không có phải hỏi lại để người dùng cung cấp đầy đủ thông tin
    startdate = datetime.strptime(startdate, "%Y-%m-%dT%H:%M:%S")
    enddate = datetime.strptime(enddate, "%Y-%m-%dT%H:%M:%S")
    configuration = config.get("configurable", {})

    data = {
        "userid": configuration.get('userid'),
        "startdate": int(startdate.timestamp()),
        "enddate": int(enddate.timestamp()),
        "coursename": coursename
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