from flask import request, jsonify
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from models.users import UserModel
from schemas.users import UserSchema


class UserRegister(Resource):
    def post(self):
        data = request.json

        user_schema = UserSchema()
        try:
            user_schema.load(data)
        except ValidationError as err:
            return err.messages

        if UserModel.find_by_username(data['username']):
            return {'message': 'Username already exists'}, 400

        user = UserModel(**data)

        try:
            user.save_to_db()
        except:
            return {'message': 'Internal error, user not created'}, 500

        return {'message': 'User created successfully'}, 201


# class User(Resource):
#     @classmethod
#     def get(cls, user_id):
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             return {'message': 'User not found!'}, 404
#         user_schema = UserSchema()
#         return user_schema.dump(user)
#
#     @classmethod
#     def delete(cls, user_id):
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             return {'message': 'User not found!'}, 404
#         user.delete_from_db()
#         return {'message': 'User successfully deleted.'}, 200
