import json
import pytest


def header_format(access_token):
    return {"Authorization": "Bearer {}".format(access_token)}


def create_item(item_name, url, client, access_token, description='desc1'):
    response = client.post(url,
                           data=json.dumps(dict(name=item_name,
                                                description=description)),
                           content_type='application/json',
                           headers=header_format(access_token))
    return response


def edit_item(item_name, category_id, url, client,
              access_token, description='desc1'):
    response = client.put(url,
                          data=json.dumps(dict(name=item_name,
                                               description=description,
                                               category_id=category_id)),
                          content_type='application/json',
                          headers=header_format(access_token))
    return response


def delete_item(url, client, access_token):
    response = client.delete(url,
                             headers=header_format(access_token))
    return response


def test_fail_create_new_item_with_duplicate_name(client, get_access_token):
    url = '/categories/1/items'
    response = create_item('Item1', url, client, get_access_token)
    assert response.status_code == 201
    response = create_item('Item1', url, client, get_access_token)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Item name already exists in '
                                              'destination category'}


def test_fail_create_new_item_in_invalid_category(client, get_access_token):
    url = '/categories/1000/items'
    response = create_item('Item2', url, client, get_access_token)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Category not found'}


def test_create_new_item_successfully(client, get_access_token):
    url = '/categories/1/items'
    response = create_item('Item2', url, client, get_access_token)
    assert response.status_code == 201


def test_fail_edit_item_in_invalid_category(client, get_access_token):
    url1 = '/categories/100/items/1'
    response = edit_item('ItemInvCat', 2, url1, client, get_access_token)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Category not found'}


def test_fail_edit_invalid_item(client, get_access_token):
    url1 = '/categories/1/items/100'
    response = edit_item('ItemInvItem', 2, url1, client, get_access_token)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Item not found'}


def test_edit_item_successfully(client, get_access_token):
    url = '/categories/1/items'
    create_item('ItemToEdit', url, client, get_access_token)
    url1 = '/categories/1/items/3'
    response = edit_item('Item3', 2, url1, client, get_access_token)
    assert response.status_code == 200
    assert response.get_json()['category_id'] == 2


def test_fail_edit_item_to_new_category_with_duplicate_name(client,
                                                            get_access_token):
    url = '/categories/1/items'
    response = create_item('Item4', url, client, get_access_token)
    assert response.status_code == 201

    url = '/categories/2/items'
    response = create_item('Item5', url, client, get_access_token)
    assert response.status_code == 201

    url1 = '/categories/1/items/4'
    response = edit_item('Item5', 2, url1, client, get_access_token)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Item name already exists '
                                              'in destination category'}


def test_fail_edit_item_with_non_item_creator_user(client, get_access_token):
    url1 = '/categories/1/items/1'
    response = edit_item('Item1', 2, url1, client, get_access_token)
    response.status_code = 403
    response.message = 'User is forbidden to perform this action ' \
                       '(user is not item creator)'


def test_get_items_from_category_successfully(client):
    url = '/categories/2/items'
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_fail_get_items_from_invalid_category(client):
    url = '/categories/100/items'
    response = client.get(url)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Category not found'}


def test_get_specific_item_successfully(client):
    url = '/categories/1/items/1'
    response = client.get(url)
    expected = {
            "id": 1,
            "name": "Item1",
            "description": "desc1",
            "category_id": 1,
            "user_id": 2
    }
    assert response.status_code == 200
    assert response.get_json() == expected


def test_fail_get_specific_item_in_invalid_category(client):
    url = '/categories/999/items/1'
    response = client.get(url)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Category not found'}


def test_fail_get_specific_invalid_item(client):
    url = '/categories/1/items/1000'
    response = client.get(url)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Item not found'}


def test_fail_get_item_exist_but_in_different_category(client):
    url = '/categories/2/items/1'
    response = client.get(url)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Item not found'}


@pytest.mark.parametrize('limit, page, order, total_items, first_item',
                         [(10, 1, 'asc', 5, 1), (1, 1, 'asc', 1, 1),
                          (2, 2, 'asc', 2, 3), (10, 1, 'desc', 5, 5),
                          (1, 1, 'desc', 1, 5), (2, 2, 'desc', 2, 3)])
def test_get_latest_items(client, limit, page, order, total_items, first_item):
    url = '/items?limit={}&page={}&order={}'.format(limit, page, order)
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()['total_items'] == total_items
    assert response.get_json()['items'][0]['id'] == first_item


def test_get_latest_items_with_invalid_order_string(client):
    url = '/items?limit=10&page=1&order=somethingwrong'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Something is '
                                              'wrong in the request'}


def test_get_latest_items_with_invalid_page_number(client):
    url = '/items?limit=10&page=-10&order=desc'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Something is '
                                              'wrong in the request'}


def test_get_latest_items_with_invalid_limit_number(client):
    url = '/items?limit=-10&page=1&order=desc'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Something is '
                                              'wrong in the request'}


def test_delete_item_in_invalid_category(client, get_access_token):
    url1 = '/categories/9999/items/1'
    response = delete_item(url1, client, get_access_token)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Category not found'}


def test_delete_invalid_item(client, get_access_token):
    url1 = '/categories/1/items/1000'
    response = delete_item(url1, client, get_access_token)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Item not found'}


def test_delete_item_from_different_category(client, get_access_token):
    url1 = '/categories/2/items/1'
    response = delete_item(url1, client, get_access_token)
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Item not found'}


def test_delete_item_with_non_item_creator_user(client, get_access_token):
    url1 = '/categories/1/items/1'
    response = delete_item(url1, client, get_access_token)
    response.status_code = 403
    response.message = 'User is forbidden to perform this action ' \
                       '(user is not item creator)'


def test_delete_item_successfully(client, get_access_token):
    url = '/categories/1/items'
    create_item('ItemToDelete', url, client, get_access_token)
    url1 = '/categories/1/items/6'
    response = delete_item(url1, client, get_access_token)
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item deleted successfully'}
