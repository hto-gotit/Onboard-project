import pytest
from flask_restful import Api
from flask_jwt_extended import JWTManager
import json
from flask import Flask

from models.categories import CategoryModel
from db import db
from resources.items import Item, AllItems, CategoryItems
from resources.users import UserRegister
from resources.login import UserLogin
from resources.categories import CategoryList


@pytest.fixture(autouse=True)
def app():
    app = Flask(__name__)
    app.config.from_envvar('ENV')
    api = Api(app)
    JWTManager(app)
    api.add_resource(CategoryItems, '/categories/<int:category_id>/items')
    api.add_resource(Item, '/categories/<int:category_id>/items/<int:item_id>')
    api.add_resource(AllItems, '/items')
    api.add_resource(UserRegister, '/users')
    api.add_resource(UserLogin, '/auth/login')
    api.add_resource(CategoryList, '/categories')
    return app


@pytest.fixture(autouse=True)
def database(app):
    db.init_app(app)
    with app.app_context():
        db.session.close()
        db.drop_all()
        db.create_all()
        CategoryModel("First category").save_to_db()
        CategoryModel("Second category").save_to_db()


@pytest.fixture()
def client(app):
    client = app.test_client()
    return client


@pytest.fixture()
def login_helper(client):
    url = '/users'
    client.post(url,
                data=json.dumps(dict(username='user1',
                                     password='pass1')),
                content_type='application/json')
    url = '/auth/login'
    response = client.post(url,
                           data=json.dumps(dict(username='user1',
                                                password='pass1')),
                           content_type='application/json')
    access_token = response.get_json()['access_token']
    return access_token
