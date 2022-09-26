from flask import Flask, request, Response, jsonify
from models import Worker
from models import Customer
from repository import ShelterRepository, WorkerRepository, CustomerRepository
import config

app = Flask(__name__)


@app.get('/')
def index():
    return 'hello'


@app.get('/animals_type_list')
def animals_type_list():
    repo = ShelterRepository()

    return repo.get_animal_types(config.get_connection())


@app.get('/workers')
def all_workers():
    repo = WorkerRepository(config.get_connection())

    return repo.all()


@app.get('/customers')
def all_customers():
    repo = CustomerRepository(config.get_connection())

    return repo.all()


@app.post('/create_worker')
def create_worker():
    data = request.get_json()
    worker = Worker(**data)

    repo = WorkerRepository(config.get_connection())
    repo.add(worker)

    return Response(status=200)


@app.post('/create_customer')
def create_customer():
    data = request.get_json()
    customer = Customer(**data)

    repo = CustomerRepository(config.get_connection())
    repo.add(customer)

    return Response(status=200)


@app.get('/get_worker')
def get_worker():
    args = request.args
    id_obj = dict(args)['id_obj']

    repo = WorkerRepository(config.get_connection())
    worker = repo.get(id_obj)

    return jsonify(worker)


@app.get('/get_customer')
def get_customer():
    args = request.args
    id_obj = dict(args)['id_obj']

    repo = CustomerRepository(config.get_connection())
    customer = repo.get(id_obj)

    return jsonify(customer)


@app.delete('/delete_worker')
def delete_worker():
    args = request.args
    id_obj = dict(args)['id_obj']

    repo = WorkerRepository(config.get_connection())
    repo.delete(id_obj)

    return Response(status=200)


@app.delete('/delete_customer')
def delete_customer():
    args = request.args
    id_obj = dict(args)['id_obj']

    repo = CustomerRepository(config.get_connection())
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


@app.get('/is_exists_customer')
def is_exists_customer():
    args = request.args
    log = dict(args)['login']
    passw = dict(args)['password']

    repo = CustomerRepository(config.get_connection())
    login = repo.get(log)
    password = repo.get(passw)

    return jsonify(login, password)