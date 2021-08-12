from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from models.users import UserModel


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = request.json

        if 'username' not in data:
            return {'message': 'Lacking field username'}, 400
        user = UserModel.find_by_username(data['username'])
        if user and user.password == data['password']:
            try:
                access_token = create_access_token(identity=user.id, fresh=True)
                return {'access_token': access_token}, 200
            except:
                return {'message': 'Internal error, login unsuccessful'}, 500
        return {'message': 'Invalid credentials'}, 400
