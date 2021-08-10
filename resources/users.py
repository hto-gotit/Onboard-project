from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from models.users import UserModel

user_parser = reqparse.RequestParser()


class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'Username already exists'}, 400
        user = UserModel(**data)
        try:
            user.save_to_db()
        except:
            {'message': 'Internal error, user was not created'}, 500
        return {'message': 'User created successfully'}, 201

