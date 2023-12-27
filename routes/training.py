from flask import Blueprint,render_template,request
from controller.trainingController import TrainingController
training = Blueprint('training', __name__)
training_controller = TrainingController
@training.route('/api/training', methods=['POST'])
def training_query():
    return TrainingController().process_create(request)

@training.route('/view/import')
def view_import():
    return render_template('import.html')

@training.route('/view/index')
def view_training_data():
    return render_template('training.html')

@training.route('/api/get_data', methods=['GET'])
def get_training_data():
    return TrainingController().get_training_data()

@training.route('/api/delete/<id>', methods=['GET'])
def delete_data():
    return TrainingController().delete_training_data(id)

@training.route('/api/import', methods=['POST'])
def handle_import():
    return TrainingController().process_import(request)
