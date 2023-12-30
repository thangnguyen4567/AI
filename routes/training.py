from flask import Blueprint,render_template,request
from controller.trainingController import TrainingController
training = Blueprint('training', __name__)
training_controller = TrainingController

@training.route('/view/import')
def view_import():
    return render_template('import.html')

@training.route('/view/index')
def view_training_data():
    return render_template('training.html')

@training.route('/api/get_training_sql', methods=['GET'])
def get_training_sql():
    return TrainingController().get_training_sql()

@training.route('/api/get_training_ddl', methods=['GET'])
def get_training_ddl():
    return TrainingController().get_training_ddl()

@training.route('/api/delete', methods=['POST'])
def delete_data():
    return TrainingController().delete_training_data(request)

@training.route('/api/import', methods=['POST'])
def handle_import():
    return TrainingController().process_import(request)

@training.route('/api/update', methods=['POST'])
def update_data():
    return TrainingController().update_training_data(request)

@training.route('/api/training', methods=['POST'])
def create_data():
    return TrainingController().create_training_data(request)

@training.route('/api/generate_table_ddl', methods=['POST'])
def generate_table_ddl():
    return TrainingController().generate_table_ddl(request)