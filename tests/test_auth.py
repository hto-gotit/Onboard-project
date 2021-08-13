import pytest
import requests
from flask import Flask
import json

from models.users import UserModel
from models.items import ItemModel
from models.categories import CategoryModel


# Tests for creating users and logging user in
def test_register_and_login():
    # Setup
    url = 'http://127.0.0.1:5000/users'
    mock_request_headers = {
        'Content-Type': 'application/json'
    }
    user1 = UserModel("user1", "pass1")

    # Create a new user test, success test
    mock_request_data = {
        'username': user1.username,
        'password': user1.password
    }
    response1 = requests.post(url,
                              data=json.dumps(mock_request_data),
                              headers=mock_request_headers)
    assert response1.json() == {'message': 'User created successfully'}
    assert response1.status_code == 201

    # Create a user with the same name, fail test
    user_same_name = UserModel("user1", "erewrwerio")
    mock_request_data_same = {
        'username': user_same_name.username,
        'password': user_same_name.password
    }
    response_same = requests.post(url,
                                  data=json.dumps(mock_request_data_same),
                                  headers=mock_request_headers)
    assert response_same.json() == {'message': 'Username already exists'}
    assert response_same.status_code == 400

    # Test login setup
    url_login = 'http://127.0.0.1:5000/auth/login'
    mock_request_wrong_format = {
        "not_username": "user1",
        "password": "pass1"
    }
    mock_request_username_none = {
        "username": "Not in database",
        "password": "pass1"
    }
    mock_request_wrong_pass = {
        "username": "user1",
        "password": "wrong_pass"
    }

    # Test login fails (lacking fields, invalid username, invalid password)
    response_login = requests.post(url_login,
                                   data=json.dumps(mock_request_wrong_format),
                                   headers=mock_request_headers)
    assert response_login.json() == {'message': 'Lacking field username'}
    assert response_login.status_code == 400

    response_login = requests.post(url_login,
                                   data=json.dumps(mock_request_username_none),
                                   headers=mock_request_headers)
    assert response_login.json() == {'message': 'Invalid username'}
    assert response_login.status_code == 400

    response_login = requests.post(url_login,
                                   data=json.dumps(mock_request_wrong_pass),
                                   headers=mock_request_headers)
    assert response_login.json() == {'message': 'Invalid password'}
    assert response_login.status_code == 400

    # Test login success
    response_login = requests.post(url_login,
                                   data=json.dumps(mock_request_data),
                                   headers=mock_request_headers)
    assert response_login.status_code == 200
