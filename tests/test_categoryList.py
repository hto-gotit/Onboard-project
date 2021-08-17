import pytest
from flask_restful import Api

import json
from flask import Flask

from models.users import UserModel
from models.items import ItemModel
from models.categories import CategoryModel
from db import db

from resources.categories import CategoryList
from config import config_test


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] \
        = 'mysql+pymysql://{}:{}@{}/{}'.format(config_test.mySQLusername,
                                               config_test.mySQLpassword,
                                               config_test.host,
                                               config_test.dbname)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] \
        = config_test.trackModification
    app.config['TESTING'] = True

    client = app.test_client()
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        cat1 = CategoryModel("First category")
        cat2 = CategoryModel("Second category")
        cat1.save_to_db()
        cat2.save_to_db()

    api = Api(app)
    api.add_resource(CategoryList, '/categories')
    return client


def test_get_categories(client):
    expected = [
        {
            "id": 1,
            "name": "First category"
        },
        {
            "id": 2,
            "name": "Second category"
        }
    ]
    url = '/categories'
    response = client.get(url)
    assert response.get_json() == expected
    assert response.status_code == 200

