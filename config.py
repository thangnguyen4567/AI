from os import path, environ

BASE_DIR = path.abspath(path.dirname(__file__))

class ConfigDB:
    SECRET_KEY = 'verysecretkey'
    CONNECT_DB = False
    SQLDATABASE_URI = 'mssql+pyodbc://ebm:4OcDQ4OLo5eGngU@103.127.207.180,3968/EBM_CRM_TEST_SE?driver=ODBC+Driver+17+for+SQL+Server'
    SQLDATABASE_INCLUDE_TABLES = ["Division","Class","Student","StudentAbsent", "StudentDept", "StudentClass", "StudentClassFee", "TrackClass"]