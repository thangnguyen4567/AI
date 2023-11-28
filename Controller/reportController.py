from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain
from flask import current_app
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.schema import Document
from langchain.vectorstores import faiss
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents.agent_toolkits import create_retriever_tool
load_dotenv('.env')


def get_conversation_query_sql(request):
    with current_app.app_context():
        app = current_app
    requestJson = request.get_json()
    userQuestion = requestJson["question"]
    configDataBase = app.config_class
    answerQuery = query_sql_database(configDataBase, userQuestion)
    answer = answerQuery.replace("\n", " ")
    result = {'question': userQuestion, 'answer': answer}
    return result

def query_sql_database(configDataBase, userQuestion):
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0)
    # llm = ChatOpenAI(model="gpt-4-32k-0314",temperature=0)
    chain = create_sql_query_chain(llm, configDataBase)
    query = chain.invoke({"question": userQuestion})
    return query

def get_conversation_query_sql_toolkit(request):
    embeddings = OpenAIEmbeddings(disallowed_special=())
    with current_app.app_context():
        app = current_app

    few_shots = {
        "Danh sách học viên trong khóa học": """SELECT c.fullname,c.id,c.shortname,c.enddate,c.renew 
                                                FROM mdl_role_assignments AS ra
                                                    JOIN mdl_user AS u ON u.id= ra.userid
                                                    JOIN mdl_user_enrolments AS ue ON ue.userid=u.id
                                                    JOIN mdl_enrol AS e ON e.id=ue.enrolid
                                                    JOIN mdl_course AS c ON c.id=e.courseid
                                                    JOIN mdl_context AS ct ON ct.id=ra.contextid AND ct.instanceid= c.id
                                                    JOIN mdl_role AS r ON r.id= ra.roleid 
                                                WHERE ra.roleid = 5""",
    }
    few_shot_docs = [
        Document(page_content=question, metadata={"sql_query": few_shots[question]})
        for question in few_shots.keys()
    ]
    vector_db = faiss.FAISS.from_documents(few_shot_docs, embeddings)
    retriever = vector_db.as_retriever()
    tool_description = """
    This tool will help you understand similar examples to adapt them to the user question.
    Input to this tool should be the user question.
    """
    retriever_tool = create_retriever_tool(
        retriever, name="sql_get_similar_examples", description=tool_description
    )
    custom_tool_list = [retriever_tool]
    custom_suffix = """
    I should first get the similar examples I know.
    If the examples are enough to construct the query, I can build it.
    Otherwise, I can then look at the tables in the database to see what I can query.
    Then I should query the schema of the most relevant tables
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo",temperature=0)
    toolkit = SQLDatabaseToolkit(db=app.config_class, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        extra_tools=custom_tool_list,
        suffix=custom_suffix,
    )
    result = agent.run("Danh sách học viên trong khóa xAPI Test")
    return result