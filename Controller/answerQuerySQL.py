from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains import create_sql_query_chain

load_dotenv('.env')

def get_conversation_query_sql(requestJson, configDataBase, check_connect):
    connectString = requestJson["connectString"]
    configTableDB = requestJson["configTableDB"]
    userQuestion = requestJson["question"]

    if check_connect == False :
        configDataBase = config_sql_database(connectString, configTableDB, check_connect)

    answerQuery = query_sql_database(configDataBase, userQuestion)

    return answerQuery

def config_sql_database(connectString, config_TableDB, checkConnect):

    # connectString = "vnr:rUbTwiQ8Rb6OEL4@115.73.215.48,16968:1433/LMS_MISA_TEST"
    conn_str = f"mssql+pyodbc://" + connectString + "?driver=ODBC+Driver+17+for+SQL+Server"
    conf_table = ["mdl_user","mdl_course","mdl_course_completions","mdl_course_modules",
                                            "mdl_course_modules_completion","mdl_modules","mdl_quiz","mdl_quiz_attempts"]
    configDataBase = SQLDatabase.from_uri(conn_str,
                            sample_rows_in_table_info=1,
                            include_tables=config_TableDB)
                            #   include_tables=["mdl_user","mdl_course","mdl_course_completions","mdl_course_modules",
                            #                   "mdl_course_modules_completion","mdl_modules","mdl_quiz","mdl_quiz_attempts"])
        
    return configDataBase

def query_sql_database(configDataBase, userQuestion):
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0)
    # llm = ChatOpenAI(model="gpt-4-32k-0314",temperature=0)
    
    chain = create_sql_query_chain(llm, configDataBase)
    query = chain.invoke({"question": userQuestion})
    
    return query