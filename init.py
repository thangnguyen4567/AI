from flask import Flask,current_app
from flask_cors import CORS
from langchain.sql_database import SQLDatabase

def create_app():
    SQLDATABASE_URI = 'mssql+pyodbc://ebm:4OcDQ4OLo5eGngU@103.127.207.180,3968/EBM_TEST_QC?driver=ODBC+Driver+17+for+SQL+Server'
    SQLDATABASE_INCLUDE_TABLES = ["Division","Class","Student","StudentAbsent", "StudentDept", "StudentClass", "StudentClassFee", "TrackClass", "BillOfSale", "BillOfSaleDetail", "BillOfSalePayment", "BillOfSalePaymentDetail"]
    app = Flask(__name__, template_folder="view")
    app.cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    with app.app_context():
        current_app.config_class = SQLDatabase.from_uri(SQLDATABASE_URI,
                                                        sample_rows_in_table_info=1,
                                                        include_tables=SQLDATABASE_INCLUDE_TABLES)
    return app 
