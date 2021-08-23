from conftest import register_or_login_user


def test_register_new_user_successfully(client):
    response = register_or_login_user('user1', 'pass1', 'register', client)
    assert response.get_json() == {'message': 'User created successfully'}
    assert response.status_code == 201


def test_failed_to_register_new_user_with_a_duplicate_name(client):
    response = register_or_login_user('user1', 'pass1', 'register', client)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Username already exists'}


def test_login_successfully(client):
    response = register_or_login_user('user1', 'pass1', 'login', client)
    assert 'access_token' in response.get_json()
    assert response.status_code == 200


def test_failed_to_login_with_invalid_username(client):
    response = register_or_login_user('user1111', 'pass1', 'login', client)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Invalid username or password'}


def test_failed_to_login_with_invalid_password(client):
    response = register_or_login_user('user1', 'wrongpassword', 'login', client)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Invalid username or password'}
