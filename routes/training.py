from flask import Blueprint,render_template,request
from llm.factory.training_factory import TrainingFactory
from config.config_vectordb import VectorDB
training = Blueprint('training', __name__)
training_factory = TrainingFactory()

@training.route('/view/index')
def view_training_data():
    data = request.args
    training = training_factory.create_training(request.args['type'])
    return render_template('training_view.html',data={'type':data['type'],'columns':training.columns})

@training.route('/api/read', methods=['GET'])
def get_training_data():
    data = request.args
    training = training_factory.create_training(request.args['type'])
    return training.get_training_data(data['index'])

@training.route('/api/training', methods=['POST'])
def save_training_data():
    data = request.get_json() 
    training = training_factory.create_training(data['type'])
    return training.save_training_data(data)
    
@training.route('/api/delete', methods=['POST'])
def delete_training_data():
    training = training_factory.create_training(request.args['type'])
    return training.delete_training_data(request.form['id'])

@training.route('/api/read_index', methods=['GET']) 
def get_index():
    data = request.args
    list_index = VectorDB().get_list_index()
    data = []
    for index in list_index:
        obj = {}
        obj['text'] = index
        obj['value'] = index
        data.append(obj)
    return data

@training.route('/api/update', methods=['POST'])
def update_data():
    data = request.form
    training = training_factory.create_training(request.args['type'])
    return training.update_training_data(data)

# @training.route('/api/generate_table_ddl', methods=['POST'])
# def generate_table_ddl():
#     return TrainingController().generate_table_ddl(request)

# @training.route('/api/get_table', methods=['GET'])
# def get_table():
#     return SQLDB().get_table()

# @training.route('/api/get_table_ddl/<table>', methods=['GET'])
# def get_table_ddl(table):
#     sql_statement = SQLDB().autogenerate_ddl(table)
#     return str(sql_statement)