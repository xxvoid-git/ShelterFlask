from flask import request, Response, jsonify, Blueprint

from src import config
from src.adapters.repository import WorkerRepository
from src.models import Worker
from src.auth import auth_decorator


app = Blueprint('worker', __name__)


@app.get('/workers')
@auth_decorator(['admin'])
def all_workers():
    repo = WorkerRepository(config.get_connection())

    return repo.all()


@app.post('/create_worker')
@auth_decorator(['admin'])
def create_worker():
    data = request.get_json()
    worker = Worker(**data)

    repo = WorkerRepository(config.get_connection())
    repo.add(worker)

    return Response(status=200)


@app.get('/get_worker')
def get_worker():
    args = request.args
    id_obj = dict(args)['id_obj']

    repo = WorkerRepository(config.get_connection())
    worker = repo.get(id_obj)

    return jsonify(worker)


@app.delete('/delete_worker')
@auth_decorator()
def delete_worker():
    args = request.args
    id_obj = dict(args)['id_obj']

    repo = WorkerRepository(config.get_connection())
    repo.delete(id_obj)

    return Response(status=200)


@app.get('/is_exists_worker')
def is_exists_worker():
    args = request.args
    log = dict(args)['login']
    passw = dict(args)['password']

    repo = WorkerRepository(config.get_connection())
    login = repo.get(log)
    password = repo.get(passw)

    return jsonify(login, password)
