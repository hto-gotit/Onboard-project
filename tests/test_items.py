import pytest
from flask_restful import Api
from flask_jwt_extended import JWTManager
import json
from flask import Flask

from models.users import UserModel
from models.items import ItemModel
from models.categories import CategoryModel
from db import db

from resources.items import Item, AllItems, CategoryItems
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
        cat1 = CategoryModel("First category")
        cat2 = CategoryModel("Second category")
        cat1.save_to_db()
        cat2.save_to_db()

    api = Api(app)
    api.add_resource(CategoryItems, '/categories/<int:category_id>/items')
    api.add_resource(Item, '/categories/<int:category_id>/items/<int:item_id>')
    api.add_resource(AllItems, '/items')
    api.add_resource(UserRegister, '/users')
    api.add_resource(UserLogin, '/auth/login')
    jwt = JWTManager(app)
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


def help_creating_item(item_name, url, client, access_token):
    response = client.post(url,
                           data=json.dumps(dict(name=item_name,
                                                description='description1')),
                           content_type='application/json',
                           headers={"Authorization":
                                        "Bearer {}".format(access_token)})
    return response


def test_create_item_success(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201


def test_create_item_invalid_category(client, login_helper):
    url = '/categories/1000/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 404


def test_create_item_duplicate_name(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 400


def test_edit_item_success(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201
    url1 = '/categories/1/items/1'
    response = client.put(url1,
                          data=json.dumps(dict(name='Item1',
                                               description='description1',
                                               category_id=2)),
                          content_type='application/json',
                          headers={"Authorization":
                                   "Bearer {}".format(login_helper)})
    assert response.status_code == 200
    assert response.get_json()['category_id'] == 2


def test_edit_item_invalid_category(client, login_helper):
    url1 = '/categories/100/items/1'
    response = client.put(url1,
                          data=json.dumps(dict(name='Item1',
                                               description='description1',
                                               category_id=2)),
                          content_type='application/json',
                          headers={"Authorization":
                                   "Bearer {}".format(login_helper)})
    assert response.status_code == 404


def test_edit_item_invalid_item(client, login_helper):
    url1 = '/categories/1/items/100'
    response = client.put(url1,
                          data=json.dumps(dict(name='Item1',
                                               description='description1',
                                               category_id=2)),
                          content_type='application/json',
                          headers={"Authorization":
                                   "Bearer {}".format(login_helper)})
    assert response.status_code == 404


def test_edit_item_duplicate_name(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201

    url = '/categories/2/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201

    url1 = '/categories/1/items/1'
    response = client.put(url1,
                          data=json.dumps(dict(name='Item1',
                                               description='description1',
                                               category_id=2)),
                          content_type='application/json',
                          headers={"Authorization":
                                   "Bearer {}".format(login_helper)})
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Item name already exists '
                                              'in destination category'}


def test_edit_item_not_creator(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201

    url = '/users'
    client.post(url,
                data=json.dumps(dict(username='user2',
                                     password='pass2')),
                content_type='application/json')
    url = '/auth/login'
    response = client.post(url,
                           data=json.dumps(dict(username='user2',
                                                password='pass2')),
                           content_type='application/json')
    access_token2 = response.get_json()['access_token']

    url1 = '/categories/1/items/1'
    response = client.put(url1,
                          data=json.dumps(dict(name='Item1',
                                               description='description1',
                                               category_id=2)),
                          content_type='application/json',
                          headers={"Authorization":
                                   "Bearer {}".format(access_token2)})
    assert response.status_code == 403


def test_delete_item_success(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201
    url1 = '/categories/1/items/1'
    response = client.delete(url1,
                             headers={"Authorization":
                                          "Bearer {}".format(login_helper)})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item deleted'}


def test_delete_item_invalid_category(client, login_helper):
    url1 = '/categories/9999/items/1'
    response = client.delete(url1,
                            headers={"Authorization":
                                     "Bearer {}".format(login_helper)})
    assert response.status_code == 404


def test_delete_item_is_none(client, login_helper):
    url1 = '/categories/1/items/1000'
    response = client.delete(url1,
                            headers={"Authorization":
                                     "Bearer {}".format(login_helper)})
    assert response.status_code == 404


def test_delete_item_different_category(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201

    url1 = '/categories/2/items/1'
    response = client.delete(url1,
                            headers={"Authorization":
                                     "Bearer {}".format(login_helper)})
    assert response.status_code == 404


def test_delete_item_not_creator(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201

    url = '/users'
    client.post(url,
                data=json.dumps(dict(username='user2',
                                     password='pass2')),
                content_type='application/json')
    url = '/auth/login'
    response = client.post(url,
                           data=json.dumps(dict(username='user2',
                                                password='pass2')),
                           content_type='application/json')
    access_token2 = response.get_json()['access_token']

    url1 = '/categories/1/items/1'
    response = client.delete(url1,
                          headers={"Authorization":
                                   "Bearer {}".format(access_token2)})
    assert response.status_code == 403


def test_get_items_from_category_success(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)

    assert response.status_code == 201
    response = client.get(url)
    assert response.status_code == 200
    expected = [
        {
            "id": 1,
            "name": "Item1",
            "description": "description1",
            "category_id": 1,
            "user_id": 1
        }
    ]
    assert response.get_json() == expected


def test_get_items_from_invalid_category(client):
    url = '/categories/100/items'
    response = client.get(url)
    assert response.status_code == 404


def test_get_specific_item_success(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201
    url = '/categories/1/items/1'
    response = client.get(url)
    expected = {
            "id": 1,
            "name": "Item1",
            "description": "description1",
            "category_id": 1,
            "user_id": 1
    }
    assert response.status_code == 200
    assert response.get_json() == expected


def test_get_specific_item_invalid_category(client):
    url = '/categories/999/items/1'
    response = client.get(url)
    assert response.status_code == 404


def test_get_item_is_none(client):
    url = '/categories/1/items/1'
    response = client.get(url)
    assert response.status_code == 404


def test_get_item_exist_different_category(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201
    url = '/categories/2/items/1'
    response = client.get(url)
    assert response.status_code == 404


def test_get_latest_items_success_asc_all_1page(client, login_helper):
    url = '/categories/1/items'
    help_creating_item('Item1', url, client, login_helper)
    help_creating_item('Item2', url, client, login_helper)
    help_creating_item('Item3', url, client, login_helper)
    url = '/items?limit=10&page=1&order=asc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()[0]['total_items'] == 3
    assert response.get_json()[0]['items'][0]['id'] == 1


def test_get_latest_items_success_desc_all_1page(client, login_helper):
    url = '/categories/1/items'
    help_creating_item('Item1', url, client, login_helper)
    help_creating_item('Item2', url, client, login_helper)
    help_creating_item('Item3', url, client, login_helper)
    url = '/items?limit=10&page=1&order=desc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()[0]['total_items'] == 3
    assert response.get_json()[0]['items'][0]['id'] == 3


def test_get_latest_items_success_asc_1limit_1page(client, login_helper):
    url = '/categories/1/items'
    help_creating_item('Item1', url, client, login_helper)
    help_creating_item('Item2', url, client, login_helper)
    help_creating_item('Item3', url, client, login_helper)
    url = '/items?limit=1&page=1&order=asc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()[0]['total_items'] == 1
    assert response.get_json()[0]['items'][0]['id'] == 1


def test_get_latest_items_success_desc_1limit_1page(client, login_helper):
    url = '/categories/1/items'
    help_creating_item('Item1', url, client, login_helper)
    help_creating_item('Item2', url, client, login_helper)
    help_creating_item('Item3', url, client, login_helper)
    url = '/items?limit=1&page=1&order=desc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()[0]['total_items'] == 1
    assert response.get_json()[0]['items'][0]['id'] == 3


def test_get_latest_items_success_asc_1limit_2page(client, login_helper):
    url = '/categories/1/items'
    help_creating_item('Item1', url, client, login_helper)
    help_creating_item('Item2', url, client, login_helper)
    help_creating_item('Item3', url, client, login_helper)
    url = '/items?limit=1&page=2&order=asc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()[0]['total_items'] == 1
    assert response.get_json()[0]['items'][0]['id'] == 1
    assert response.get_json()[1]['total_items'] == 1
    assert response.get_json()[1]['items'][0]['id'] == 2


def test_get_latest_items_success_desc_1limit_2page(client, login_helper):
    url = '/categories/1/items'
    help_creating_item('Item1', url, client, login_helper)
    help_creating_item('Item2', url, client, login_helper)
    help_creating_item('Item3', url, client, login_helper)
    url = '/items?limit=1&page=2&order=desc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()[0]['total_items'] == 1
    assert response.get_json()[0]['items'][0]['id'] == 3
    assert response.get_json()[1]['total_items'] == 1
    assert response.get_json()[1]['items'][0]['id'] == 2


def test_get_latest_items_invalid_order(client):
    url = '/items?limit=10&page=1&order=somethingwrong'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Order parameter not recognized'}


def test_get_latest_items_invalid_page(client, login_helper):
    url = '/items?limit=10&page=-10&order=desc'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'limit and page must be positive'}


def test_get_latest_items_invalid_limit(client, login_helper):
    url = '/items?limit=-10&page=1&order=desc'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'limit and page must be positive'}
