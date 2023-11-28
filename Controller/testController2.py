from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain
from flask import current_app
from langchain_experimental.sql.vector_sql import VectorSQLDatabaseChain
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
load_dotenv('.env')
def test(request):
    requestJson = request.get_json()
    userQuestion = requestJson["question"]
    examples = [
        {
            "question": "Danh sách học viên nghỉ học tháng 10 năm 2023 theo lớp học ? (IsAbsent 1:Nghĩ học)",
            "answer":
                    """
                        SELECT SA.Date AS Ngày Vắng, S.Lastname AS Tên Học Viên, C.Name AS Tên Lớp, C.Code AS Mã Lớp, S.Id AS Id Học Viên 
                            FROM StudentAbsent AS SA 
                                JOIN Student AS S ON SA.StudentId = S.Id 
                                JOIN Class AS C ON SA.ClassId = C.Id 
                            WHERE MONTH(SA.Date) = 10 AND YEAR(SA.Date) = 2023 AND SA.IsAbsent = 1 
                            ORDER BY SA.[Date ASC
                    """
        },
        {
            "question": "DS lớp của học viên đang học trong lớp ? (Status 1:đang học 2:ngưng học) (TypeStudentClass 0: Bình thường 1: Học lại 2: Nợ phí)",
            "answer": 
                    """
                        Select st.Id as "StudentId", st.Lastname, cl.Name as "ClassName",sc.DateFrom, sc.DateTo, sc.Status as "StatusStudentClass", dv.DivisionName 
                        from StudentClass sc 
                            left join Class cl on cl.Id = sc.ClassId
                            left join Division dv on dv.Id = cl.DivisionID
                            left join Student st on st.Id = sc.StudentId
                    """
        },
        {
            "question": "DS học viên có đi học và nội dung bài học của ngày hôm đó?",
            "answer":
                    """
                        select sc.StudentId,st.Lastname,sa.IsAbsent,tc.id as "TrackClassId", cl.Name as "ClassName", dv.DivisionName, tc.LessonContent, tc.TrackDate 
                        from TrackClass tc
                            left join Class cl on cl.Id = tc.ClassId
                            left join Division dv on dv.Id = cl.DivisionID
                            left join StudentClass sc on tc.ClassId = sc.ClassId 
                            left join Student st on st.Id = sc.StudentId
                            left join StudentAbsent sa on sa.ClassId = sc.ClassId and sa.StudentId = sc.StudentId and sa.TrackClassId = tc.id
                        where tc.TrackDate = '2023-08-21 00:00:00.000'
                        and (sa.IsAbsent != 1 or sa.id is null)
                    """
        }
    ]
    example_prompt = PromptTemplate(input_variables=["question", "answer"], template="When query compare name add N'' Question: {question}\n{answer}")
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix="Question: {input}",
        input_variables=["input"]
    )
    with current_app.app_context():
        app = current_app
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0)
    chain = create_sql_query_chain(llm, app.config_class)
    query = chain.invoke({"question": prompt.format(input=userQuestion)})
    print(query)
    answer = query.replace("\n", "")
    return answer