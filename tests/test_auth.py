import pytest
from flask_restful import Api
from flask_jwt_extended import JWTManager
import json
from flask import Flask

from models.users import UserModel
from models.items import ItemModel
from models.categories import CategoryModel
from db import db

from resources.users import UserRegister
from resources.login import UserLogin


@pytest.fixture(autouse=True)
def client():
    app = Flask(__name__)
    app.config.from_envvar('ENV')
    client = app.test_client()
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

    api = Api(app)
    api.add_resource(UserRegister, '/users')
    api.add_resource(UserLogin, '/auth/login')
    jwt = JWTManager(app)
    return client


def help_user(username, password, url, client):
    response = client.post(url,
                           data=json.dumps(dict(username=username,
                                                password=password)),
                           content_type='application/json')
    return response


def test_register_user_success(client):
    url = '/users'
    response = help_user('user1', 'pass1', url, client)
    # response = client.post(url,
    #                        data=json.dumps(dict(username='user1',
    #                                             password='pass1')),
    #                        content_type='application/json')
    assert response.get_json() == {'message': 'User created successfully'}
    assert response.status_code == 201


def test_register_user_duplicate_name(client):
    url = '/users'
    response = help_user('user1', 'pass1', url, client)
    assert response.status_code == 201
    response = help_user('user1', 'pass1', url, client)
    assert response.status_code == 400
    assert response.get_json()['description'] == 'Username already exists'


def test_login_success(client):
    url = '/users'
    response = help_user('user1', 'pass1', url, client)
    assert response.status_code == 201
    url2 = '/auth/login'
    response = help_user('user1', 'pass1', url2, client)
    assert 'access_token' in response.get_json()
    assert response.status_code == 200


def test_login_invalid_username(client):
    url = '/users'
    response = help_user('user1', 'pass1', url, client)
    assert response.status_code == 201
    url2 = '/auth/login'
    response = help_user('user1111', 'pass1', url2, client)
    assert response.get_json()['description'] == 'Invalid username or password'
    assert response.status_code == 400


def test_login_invalid_password(client):
    url = '/users'
    response = help_user('user1', 'pass1', url, client)
    assert response.status_code == 201
    url2 = '/auth/login'
    response = help_user('user1', 'wrongpassword', url2, client)
    assert response.get_json()['description'] == 'Invalid username or password'
    assert response.status_code == 400
