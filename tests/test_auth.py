import json
import pytest
from errors import *


def register_login_user(username, password, url, client):
    response = client.post(url,
                           data=json.dumps(dict(username=username,
                                                password=password)),
                           content_type='application/json')
    return response


def test_register_user_success(client):
    url = '/users'
    response = register_login_user('user1', 'pass1', url, client)
    assert response.get_json() == {'message': 'User created successfully'}
    assert response.status_code == 201


def test_failed_register_user_duplicate_name(client, database):
    url = '/users'
    response = register_login_user('user1', 'pass1', url, client)
    assert response.status_code == 201
    with pytest.raises(UsernameAlreadyExists):
        register_login_user('user1', 'pass1', url, client)
    assert 2 == 2


def test_login_success(client):
    url = '/users'
    response = register_login_user('user1', 'pass1', url, client)
    assert response.status_code == 201
    url2 = '/auth/login'
    response = register_login_user('user1', 'pass1', url2, client)
    assert 'access_token' in response.get_json()
    assert response.status_code == 200


def test_failed_login_invalid_username(client):
    url = '/users'
    response = register_login_user('user1', 'pass1', url, client)
    assert response.status_code == 201
    url2 = '/auth/login'
    with pytest.raises(InvalidCredentials):
        register_login_user('user1111', 'pass1', url2, client)


def test_failed_login_invalid_password(client):
    url = '/users'
    response = register_login_user('user1', 'pass1', url, client)
    assert response.status_code == 201
    url2 = '/auth/login'
    with pytest.raises(InvalidCredentials):
        register_login_user('user1', 'wrongpassword', url2, client)
