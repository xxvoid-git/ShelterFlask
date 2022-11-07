from flask import request, jsonify, Response, Blueprint
from src import config
from src.adapters.repository import CustomerRepository
from src.models import Customer


app = Blueprint('customer', __name__)


@app.get('/get_customer')
def get_customer():
    args = request.args
    id_obj = dict(args)['id_obj']

    repo = CustomerRepository(config.get_connection())
    customer = repo.get(id_obj)

    return jsonify(customer)


@app.get('/customers')
def all_customers():
    repo = CustomerRepository(config.get_connection())

    return repo.all()


@app.post('/create_customer')
def create_customer():
    data = request.get_json()
    customer = Customer(**data)

    repo = CustomerRepository(config.get_connection())
    repo.add(customer)

    return Response(status=200)


@app.delete('/delete_customer')
def delete_customer():
    args = request.args
    id_obj = dict(args)['id_obj']

    repo = CustomerRepository(config.get_connection())
    repo.delete(id_obj)

    return Response(status=200)


@app.get('/is_exists_customer')
def is_exists_customer():
    args = request.args
    log = dict(args)['login']
    passw = dict(args)['password']

    repo = CustomerRepository(config.get_connection())
    ans = repo.is_exists_customer(log, passw)

    return jsonify(ans)
