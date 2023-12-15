# from controller.trainingController import TrainingController
from flask import Blueprint,render_template,request
from controller.trainingController import training_from_import

training = Blueprint('training', __name__)

@training.route('/api/training', methods=['POST'])
def training_query():
    requestJson = request.get_json()
    # question = requestJson['question']
    # query = requestJson['query']

@training.route('/view/import')
def view_import():
    return render_template('import.html')


@training.route('/api/import', methods=['POST'])
def handle_import():
    return training_from_import(request)