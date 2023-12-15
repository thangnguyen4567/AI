from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import os
import json

class SQLDB:
    def __init__(self):
        load_dotenv()
        self.db_username = os.getenv("SQLDB_USERNAME")
        self.db_password = os.getenv("SQLDB_PASSWORD")
        self.db_host = os.getenv("SQLDB_HOST")
        self.db_name = os.getenv("SQLDB_NAME")
        self.db_include_tables = os.getenv("SQLDB_INCLUDE_TABLE")

    def config_sqldb(self):
        db_uri = f"mssql+pyodbc://{self.db_username}:{self.db_password}@{self.db_host}/{self.db_name}?driver=ODBC+Driver+17+for+SQL+Server"
        sql_db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=1, include_tables=json.loads(self.db_include_tables))
        return sql_db