from flask import Flask
from flask_cors import CORS
from langchain.sql_database import SQLDatabase
from config import ConfigDB



def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secretkey'
    app.cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_object(ConfigDB)

    if app.config['CONNECT_DB'] == False:
        connect_sqldb(app)

    return app 


def connect_sqldb(app):

    sqldatabase_uri = app.config['SQLDATABASE_URI']
    sqldatabase_include_tables = app.config['SQLDATABASE_INCLUDE_TABLES']
    conn_str = sqldatabase_uri
    conf_table = sqldatabase_include_tables
    config_database = SQLDatabase.from_uri(conn_str,
                              sample_rows_in_table_info=1,
                              include_tables=conf_table)
    app.config_class = config_database
    app.config['CONNECT_DB'] = True
    
    return config_database