from flask import Blueprint,render_template,request
from llm.factory.training_factory import TrainingFactory
from controller.trainingController import TrainingController
from config.config_vectordb import VectorDB
from config.config_sqldb import SQLDB
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tools.helper import remove_stopwords
import pandas as pd

training = Blueprint('training', __name__)
training_factory = TrainingFactory()

@training.route('/training_report')
def view_training_data_v2():
    return render_template('training.html')

@training.route('/index')
def view_training_data():
    data = request.args
    training = training_factory.create_training(request.args['type'])
    return render_template('training_view.html',data={'type':data['type'],'columns':training.columns})

@training.route('/read', methods=['GET'])
def get_training_data():
    data = request.args
    training = training_factory.create_training(request.args['type'])
    return training.get_training_data(data['index'])

@training.route('/training', methods=['POST'])
def save_training_data():
    if(request.form):
        data = request.form
    else:
        data = request.get_json() 
    training = training_factory.create_training(data['type'])
    return training.save_training_data(data)
    
@training.route('/delete', methods=['POST'])
def delete_training_data():
    training = training_factory.create_training(request.args['type'])
    return training.delete_training_data(request.form['id'])

@training.route('/read_index', methods=['GET'])
def get_index():
    datatype = request.args['type']
    if datatype == 'chatbot':
        data = [
            {'text':'highlands'},
            {'text':'webcafe'},
        ]
    elif datatype == 'training_course':
        list_index = VectorDB().get_list_index()
        data = []
        for index in list_index:
            obj = {}
            obj['text'] = index
            obj['value'] = index
            data.append(obj)
    return data

@training.route('/update', methods=['POST','GET'])
def update_data():
    datatype = request.args['type']
    data = request.form
    training = training_factory.create_training(datatype)
    return training.update_training_data(data)

# @training.route('/generate_table_ddl', methods=['POST'])
# def generate_table_ddl():
#     return TrainingController().generate_table_ddl(request)

@training.route('/get_table', methods=['GET'])
def get_table():
    return SQLDB().get_table()

@training.route('/get_table_ddl/<table>', methods=['GET'])
def get_table_ddl(table):
    sql_statement = SQLDB().autogenerate_ddl(table)
    return str(sql_statement)

@training.route('/import', methods=['GET','POST'])
def import_data():
    if 'file' in request.files:
        db = request.args['db']
        file = request.files['file']
        all_sheets = pd.read_excel(file, sheet_name=None)
        finaldocx = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1400,
            chunk_overlap=100,
            length_function=len,
        )
        try:
            for sheet_name, df in all_sheets.items():
                for index, row in df.iterrows():
                    metadata = {}
                    content = remove_stopwords(row.content)
                    texts = text_splitter.split_text(content)
                    for text in texts:
                        metatext = ''
                        for column in df.columns:
                            if column != 'content' and isinstance(row[column], str) and row[column] != '':
                                metadata[column] = row[column]
                                metatext += column+':'+row[column]+','
                        finaldocx.append(Document(
                            page_content=text+metatext, 
                            metadata=metadata
                        ))
                vector_db = VectorDB()
                vector_db.add_vectordb(finaldocx,db)
            return 'Import thành công'
        except:
            return 'Import thất bại'
    return 'Import thất bại'
