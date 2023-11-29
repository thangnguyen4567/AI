from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import os
import json
load_dotenv()

def config_sqldb():
    db_username = os.getenv("SQLDB_USERNAME")
    db_password = os.getenv("SQLDB_PASSWORD")
    db_host = os.getenv("SQLDB_HOST")
    db_name = os.getenv("SQLDB_NAME")
    db_include_tables = os.getenv("SQLDB_INCLUDE_TABLE")
    db_uri = f"mssql+pyodbc://{db_username}:{db_password}@{db_host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
    sql_db = SQLDatabase.from_uri(db_uri,sample_rows_in_table_info=1,include_tables=json.loads(db_include_tables))
    return sql_db 
