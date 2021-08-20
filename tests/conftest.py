import pytest
import json
import os
import random
import string

from models.categories import CategoryModel
from db import db
from app import app


@pytest.fixture(scope='session')
def application():
    if os.environ['ENV'] != 'config\\test.cfg':
        pytest.exit("Wrong Environment!")
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        CategoryModel("First category").save_to_db()
        CategoryModel("Second category").save_to_db()
    return app


@pytest.fixture()
def client(application):
    client = application.test_client()
    return client


@pytest.fixture()
def get_access_token(client):
    username = ''.join(random.choices(string.ascii_letters, k=4))
    password = ''.join(random.choices(string.ascii_letters, k=4))
    register_or_login_user(username, password, 'register', client)
    response = register_or_login_user(username, password, 'login', client)
    access_token = response.get_json()['access_token']
    return access_token


def register_or_login_user(username, password, choice, client):
    if choice == 'login':
        url = '/auth/login'
    else:
        url = '/users'
    response = client.post(url,
                           data=json.dumps(dict(username=username,
                                                password=password)),
                           content_type='application/json')
    return response
