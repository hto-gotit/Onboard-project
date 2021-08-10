from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from models.users import UserModel

user_parser = reqparse.RequestParser()


class Login(Resource):
    def post(self):
        data = user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 400
