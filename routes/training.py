from flask import Blueprint,render_template,request
from llm.factory.training_factory import TrainingFactory
training = Blueprint('training', __name__)
training_factory = TrainingFactory()

@training.route('/view/index')
def view_training_data():
    data = request.args
    training = training_factory.create_training(data['type'])
    return render_template('training_view.html',data={'type':data['type'],'columns':training.columns})

@training.route('/api/read', methods=['GET'])
def get_training_data():
    data = request.args
    training = training_factory.create_training(data['type'])
    return training.get_training_data()

@training.route('/api/create', methods=['POST'])
def save_training_data():
    data = request.get_json() 
    training = training_factory.create_training(data['type'])
    return training.save_training_data(data)
    
@training.route('/api/delete', methods=['POST'])
def delete_training_data():
    training = training_factory.create_training(request.args.data['type'])
    return training.delete_training_data(request.form['id'])

# @training.route('/view/import')
# def view_import():
#     return render_template('import.html')

# @training.route('/api/import', methods=['POST'])
# def handle_import():
#     return TrainingController().process_import(request)

# @training.route('/api/update', methods=['POST'])
# def update_data():
#     return TrainingController().update_training_data(request)

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