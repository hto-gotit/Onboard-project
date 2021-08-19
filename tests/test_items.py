import json
import pytest
from errors import *


def help_creating_item(item_name, url, client, access_token):
    response = client.post(url,
                           data=json.dumps(dict(name=item_name,
                                                description='description1')),
                           content_type='application/json',
                           headers={"Authorization":
                                        "Bearer {}".format(access_token)})
    return response


def help_create_multiple_items(url, client, access_token):
    item_names = ['Item1', 'Item2', 'Item3', 'Item4']
    for name in item_names:
        help_creating_item(name, url, client, access_token)


def help_editing_item(item_name, category_id, url, client, access_token):
    response = client.put(url,
                          data=json.dumps(dict(name=item_name,
                                               description='description1',
                                               category_id=category_id)),
                          content_type='application/json',
                          headers={"Authorization":
                                   "Bearer {}".format(access_token)})
    return response


def help_delete_item(url, client, access_token):
    response = client.delete(url,
                             headers={"Authorization":
                                      "Bearer {}".format(access_token)})
    return response


def test_create_item_success(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201


def test_fail_create_item_invalid_category(client, login_helper):
    url = '/categories/1000/items'
    with pytest.raises(CategoryDNE):
        help_creating_item('Item1', url, client, login_helper)


def test_fail_create_item_duplicate_name(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201
    with pytest.raises(ItemNameDuplicate):
        help_creating_item('Item1', url, client, login_helper)


def test_edit_item_success(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201
    url1 = '/categories/1/items/1'
    response = help_editing_item('Item1', 2, url1, client, login_helper)
    assert response.status_code == 200
    assert response.get_json()['category_id'] == 2


def test_fail_edit_item_invalid_category(client, login_helper):
    url1 = '/categories/100/items/1'
    with pytest.raises(CategoryDNE):
        help_editing_item('Item1', 2, url1, client, login_helper)


def test_fail_edit_item_invalid_item(client, login_helper):
    url1 = '/categories/1/items/100'
    with pytest.raises(ItemDNE):
        help_editing_item('Item1', 2, url1, client, login_helper)


def test_fail_edit_item_duplicate_name(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201

    url = '/categories/2/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201

    url1 = '/categories/1/items/1'
    with pytest.raises(ItemNameDuplicate):
        help_editing_item('Item1', 2, url1, client, login_helper)


def test_fail_edit_item_not_creator(client, login_helper):
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
    with pytest.raises(UserForbidden):
        help_editing_item('Item1', 2, url1, client, access_token2)


def test_delete_item_success(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201
    url1 = '/categories/1/items/1'
    response = help_delete_item(url1, client, login_helper)
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item deleted successfully'}


def test_delete_item_invalid_category(client, login_helper):
    url1 = '/categories/9999/items/1'
    with pytest.raises(CategoryDNE):
        help_delete_item(url1, client, login_helper)


def test_delete_item_is_none(client, login_helper):
    url1 = '/categories/1/items/1000'
    with pytest.raises(ItemDNE):
        help_delete_item(url1, client, login_helper)


def test_delete_item_different_category(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201

    url1 = '/categories/2/items/1'
    with pytest.raises(ItemDNE):
        help_delete_item(url1, client, login_helper)


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
    with pytest.raises(UserForbidden):
        help_delete_item(url1, client, access_token2)


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


def test_fail_get_items_from_invalid_category(client):
    url = '/categories/100/items'
    with pytest.raises(CategoryDNE):
        client.get(url)


def test_fail_get_specific_item_success(client, login_helper):
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


def test_fail_get_specific_item_invalid_category(client):
    url = '/categories/999/items/1'
    with pytest.raises(CategoryDNE):
        client.get(url)


def test_fail_get_item_is_none(client):
    url = '/categories/1/items/1'
    with pytest.raises(ItemDNE):
        client.get(url)


def test_fail_get_item_exist_different_category(client, login_helper):
    url = '/categories/1/items'
    response = help_creating_item('Item1', url, client, login_helper)
    assert response.status_code == 201
    url = '/categories/2/items/1'
    with pytest.raises(ItemDNE):
        client.get(url)


def test_get_latest_items_success_asc_all_page1(client, login_helper):
    url = '/categories/1/items'
    help_create_multiple_items(url, client, login_helper)
    url = '/items?limit=10&page=1&order=asc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()['total_items'] == 4
    assert response.get_json()['items'][0]['id'] == 1


def test_get_latest_items_success_desc_all_page1(client, login_helper):
    url = '/categories/1/items'
    help_create_multiple_items(url, client, login_helper)
    url = '/items?limit=10&page=1&order=desc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()['total_items'] == 4
    assert response.get_json()['items'][0]['id'] == 4


def test_get_latest_items_success_asc_limit1_page1(client, login_helper):
    url = '/categories/1/items'
    help_create_multiple_items(url, client, login_helper)
    url = '/items?limit=1&page=1&order=asc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()['total_items'] == 1
    assert response.get_json()['items'][0]['id'] == 1


def test_get_latest_items_success_desc_limit1_page1(client, login_helper):
    url = '/categories/1/items'
    help_create_multiple_items(url, client, login_helper)
    url = '/items?limit=1&page=1&order=desc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()['total_items'] == 1
    assert response.get_json()['items'][0]['id'] == 4


def test_get_latest_items_success_asc_limit2_page2(client, login_helper):
    url = '/categories/1/items'
    help_create_multiple_items(url, client, login_helper)
    url = '/items?limit=2&page=2&order=asc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()['total_items'] == 2
    assert response.get_json()['items'][0]['id'] == 3
    assert response.get_json()['items'][1]['id'] == 4


def test_get_latest_items_success_desc_limit2_page2(client, login_helper):
    url = '/categories/1/items'
    help_create_multiple_items(url, client, login_helper)
    url = '/items?limit=2&page=2&order=desc'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()['total_items'] == 2
    assert response.get_json()['items'][0]['id'] == 2
    assert response.get_json()['items'][1]['id'] == 1


def test_get_latest_items_invalid_order(client):
    url = '/items?limit=10&page=1&order=somethingwrong'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Something is '
                                              'wrong in the request'}


def test_get_latest_items_invalid_page(client):
    url = '/items?limit=10&page=-10&order=desc'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Something is '
                                              'wrong in the request'}


def test_get_latest_items_invalid_limit(client):
    url = '/items?limit=-10&page=1&order=desc'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Something is '
                                              'wrong in the request'}
