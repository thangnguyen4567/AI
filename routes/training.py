from flask import Blueprint,render_template,request
from controller.trainingController import training_from_import,training_from_api
from config.config_vectordb import VectorDB

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
    docs = vector_db.connect_vectordb().similarity_search(query='',k=100)
    data = []
    for value in docs:
        obj = {}
        obj['id'] = value.metadata['id']
        obj['question'] = value.page_content
        obj['answer'] = value.metadata['query']
        obj['action'] = '<a target="_blank" href="../api/delete/'+obj['id']+'" >Xóa</a>'
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