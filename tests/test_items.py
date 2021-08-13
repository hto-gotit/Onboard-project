import pytest
import requests
import json

from models.users import UserModel
from models.items import ItemModel
from models.categories import CategoryModel


# Create some users for use in item managing
@pytest.fixture()
def user_for_manage():
    url = 'http://127.0.0.1:5000/users'
    mock_request_headers = {
        'Content-Type': 'application/json'
    }
    user_login1 = UserModel("user_login1", "pass1")
    mock_request_data = {
        'username': user_login1.username,
        'password': user_login1.password
    }
    requests.post(url, data=json.dumps(mock_request_data),
                  headers=mock_request_headers)
    user_login2 = UserModel("user_login2", "pass2")
    mock_request_data = {
        'username': user_login2.username,
        'password': user_login2.password
    }
    requests.post(url, data=json.dumps(mock_request_data),
                  headers=mock_request_headers)

    return user_login1, user_login2


# Test managing items
def test_manage_item(user_for_manage):
    # Setup
    user1, user2 = user_for_manage
    url_list_items = 'http://127.0.0.1:5000/categories/{}/items'
    url_item = 'http://127.0.0.1:5000/categories/{}/items/{}'
    url_login = 'http://127.0.0.1:5000/auth/login'

    mock_request_headers = {
        'Content-Type': 'application/json'
    }

    # Log the users in
    user1data = {
        'username': user1.username,
        'password': user1.password
    }
    user2data = {
        'username': user2.username,
        'password': user2.password
    }
    response_login = requests.post(url_login,
                                   data=json.dumps(user1data),
                                   headers=mock_request_headers)
    access_token_1 = response_login.json()['access_token']
    response_login_2 = requests.post(url_login,
                                     data=json.dumps(user2data),
                                     headers=mock_request_headers)
    access_token_2 = response_login_2.json()['access_token']
    request_headers_manage_1 = {
        'Authorization': 'Bearer {}'.format(access_token_1),
        'Content-Type': 'application/json'
    }
    request_headers_manage_2 = {
        'Authorization': 'Bearer {}'.format(access_token_2),
        'Content-Type': 'application/json'
    }

    # Create some items
    item1 = {
        'name': 'item1', 'description': 'desc1',
        'category_id': 1, 'user_id': 2
    }
    item2 = {
        'name': 'item2', 'description': 'desc2',
        'category_id': 1, 'user_id': 2
    }
    item_invalid_cate = {
        'name': 'item_in', 'description': 'desc',
         'category_id': 1000, 'user_id': 2
    }

    # Create item test successes
    response_create_1 = requests.post(url_list_items.format(1),
                                      data=json.dumps(item1),
                                      headers=request_headers_manage_1)
    response_create_2 = requests.post(url_list_items.format(1),
                                      data=json.dumps(item2),
                                      headers=request_headers_manage_1)
    assert response_create_1.status_code == 201
    assert response_create_1.json()['id'] == 1
    assert response_create_2.status_code == 201
    assert response_create_2.json()['id'] == 2

    # Create item test fail
    response_create_invalid = requests.post(url_list_items.format(1000),
                                            data=json.dumps(item_invalid_cate),
                                            headers=request_headers_manage_1)
    assert response_create_invalid.status_code == 400
    assert response_create_invalid.json() \
           == {'message': 'There is no such category'}

    # Delete item test fail
    resp_del_not_creator = requests.delete(url_item.format(1, 2),
                                           headers=request_headers_manage_2)
    assert resp_del_not_creator.status_code == 403

    # Delete item test success
    resp_del_creator = requests.delete(url_item.format(1, 2),
                                       headers=request_headers_manage_1)
    assert resp_del_creator.status_code == 200

    # Edit the info of item 1
    item1edit = {
        'name': 'item1 changed', 
        'description': 'desc1',
        'category_id': 2, 
        'user_id': 2
    }
    # Edit item fails (not creator, invalid category, item not found)
    resp_edit_no_category = requests.put(url_item.format(2021, 1),
                                         data=json.dumps(item_invalid_cate),
                                         headers=request_headers_manage_1)
    assert resp_edit_no_category.status_code == 400
    resp_edit_no_item = requests.put(url_item.format(1, 9000),
                                     data=json.dumps(item1edit),
                                     headers=request_headers_manage_1)
    assert resp_edit_no_item.status_code == 404
    resp_edit_not_creator = requests.put(url_item.format(1, 1),
                                         data=json.dumps(item1edit),
                                         headers=request_headers_manage_2)
    assert resp_edit_not_creator.status_code == 403
    resp_edit_creator = requests.put(url_item.format(1, 1),
                                     data=json.dumps(item1edit),
                                     headers=request_headers_manage_1)

    # Edit item success
    assert resp_edit_creator.status_code == 200
    assert resp_edit_creator.json()['name'] == "item1 changed"

    # Fetch the list of latest items
    url_latest = 'http://127.0.0.1:5000/items?limit={}&page={}&order={}'
    url_latest_desc = url_latest.format(2, 1, 'desc')

    requests.post(url_list_items.format(1),         # Recreate item 2
                  data=json.dumps(item2),
                  headers=request_headers_manage_1)

    # Fetch the list in descending order
    resp_get_latest = requests.get(url_latest_desc)
    assert resp_get_latest.status_code == 200
    assert resp_get_latest.json()[0]['name'] == 'item2'
    assert resp_get_latest.json()[1]['name'] == 'item1 changed'

    # Fetch the list in descending order but limit is to only 1 item
    url_latest_limit = url_latest.format(1, 1, 'desc')
    resp_get_latest_limit = requests.get(url_latest_limit)
    assert resp_get_latest_limit.status_code == 200
    try:
        resp_get_latest_limit.json()[1]
    except IndexError:
        assert True
        assert resp_get_latest_limit.json()[0]['name'] == 'item2'

    # Fetch the list in ascending order
    url_latest_asc = url_latest.format(2, 1, 'asc')
    resp_get_latest_asc = requests.get(url_latest_asc)
    assert resp_get_latest_asc.status_code == 200
    assert resp_get_latest_asc.json()[0]['name'] == 'item1 changed'
    assert resp_get_latest_asc.json()[1]['name'] == 'item2'

    # Invalid ordering argument
    url_latest_invalid = url_latest.format(2, 1, 'some_gibbrish')
    resp_get_latest_invalid = requests.get(url_latest_invalid)
    assert resp_get_latest_invalid.status_code == 400


# Tests to get the items (individual) and item lists
def test_get_item():
    url_list_items = 'http://127.0.0.1:5000/categories/{}/items'
    url_item = 'http://127.0.0.1:5000/categories/{}/items/{}'
    # Get items from a valid category
    response_get_list = requests.get(url_list_items.format(1))
    assert response_get_list.status_code == 200

    # Get items from invalid category
    response_get_list = requests.get(url_list_items.format(100))
    assert response_get_list.status_code == 404

    # Get a valid item (created above)
    response_get_item = requests.get(url_item.format(1, 1))
    assert response_get_item.status_code == 200

    # Get an invalid item
    response_get_item = requests.get(url_item.format(1, 1990))
    assert response_get_item.status_code == 404
