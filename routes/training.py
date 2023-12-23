from flask import Blueprint,render_template,request,jsonify
from controller.trainingController import training_from_import, training_from_api, training_from_query
from config.config_vectordb import VectorDB
import datetime
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
        content = r.hget(key,'content')
        query = r.hget(key,'query')
        timecreated = r.hget(key,'timecreated')
        obj['id'] = key.decode()
        obj['question'] = content.decode() if content else 'None'
        obj['answer'] = query.decode() if query else 'None'
        obj['timecreated'] = datetime.datetime.fromtimestamp(int(timecreated.decode())).strftime("%d/%m/%Y %H:%M:%S") if timecreated else '22/12/2023 00:00:00'
        obj['action'] = '<a class="delete btn btn-danger" id="'+obj['id']+'">Xóa</a>'
        data.append(obj)
    sorted_data = sorted(data, key=lambda x: x['timecreated'],reverse=True)
    return sorted_data

@training.route('/api/delete/<id>', methods=['GET'])
def delete_data(id):
    vector_db = VectorDB()
    redis_client = vector_db.connect_client()
    redis_client.delete(id)
    return id

@training.route('/api/import', methods=['POST'])
def handle_import():
    return training_from_import(request.form)

@training.route('/api/training_from', methods=['POST'])
def training_from():
    return training_from_query(request)