from flask import Blueprint,render_template,request,jsonify
from controller.trainingController import training_from_import,training_from_api
from config.config_vectordb import VectorDB
import redis

training = Blueprint('training', __name__)

@training.route('/api/training', methods=['POST'])
def training_query():
    return training_from_api(request)

@training.route('/view/import')
def view_import():
    return render_template('import.html')

@training.route('/view/index')
def view_training_data():
    return render_template('training.html')

@training.route('/api/get_data', methods=['GET'])
def get_training_data():
    vector_db = VectorDB()
    r = vector_db.connect_client()
    data = []
    for key in r.scan_iter("doc:*"):
        obj = {}
        content = r.hget(key,'content').decode()
        query = r.hget(key,'query').decode()
        timecreated = r.hget(key,'timecreated').decode()
        obj['question'] = content
        obj['answer'] = query
        obj['id'] = key.decode()
        obj['action'] = '<a class="delete btn btn-danger" id="'+obj['id']+'">Xóa</a>'
        obj['timecreated'] = timecreated
        data.append(obj)
    return data

@training.route('/api/delete/<id>', methods=['GET'])
def delete_data(id):
    vector_db = VectorDB()
    redis_client = vector_db.connect_client()
    redis_client.delete(id)
    return id

@training.route('/api/import', methods=['POST'])
def handle_import():
    return training_from_import(request)