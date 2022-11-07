from flask import Flask
from src.adapters.repository import ShelterRepository
from src.worker_endpoints import app as worker_app
from src.customer_endpoints import app as customer_app
from src import config

app = Flask(__name__)
app.register_blueprint(worker_app)
app.register_blueprint(customer_app)


@app.get('/')
def index():
    return 'hello'


@app.get('/animals_type_list')
def animals_type_list():
    repo = ShelterRepository()

    return repo.get_animal_types(config.get_connection())