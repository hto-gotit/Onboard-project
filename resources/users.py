from flask import request                   # import flask request
from flask_restful import Resource          # import resource from restful
# import class to raise errors for marshmallow
from marshmallow import ValidationError

from models.users import UserModel          # import model for user
from schemas.users import UserSchema        # import schema for user


# /users resource, used only for registering a new user
class UserRegister(Resource):
    # Function to create a new user
    @classmethod
    def post(cls):
        data = request.json                     # fetch the info of the request
        user_schema = UserSchema()              # declare the schema for user
        try:
            user_schema.load(data)              # validate the request
        except ValidationError as err:
            return err.messages

        if UserModel.find_by_username(data['username']):
            # if username already existed, return 400
            return {'message': 'Username already exists'}, 400

        user = UserModel(**data)     # username available, create a new user

        try:
            user.save_to_db()        # save the user to the database
        except:
            return {'message': 'Internal error, user not created'}, 500

        return {'message': 'User created successfully'}, 201


# /user/user_id resource (Not available to users)
# class User(Resource):
#     # Function to get id and usernam of an user
#     @classmethod
#     def get(cls, user_id):
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             return {'message': 'User not found!'}, 404
#         user_schema = UserSchema()
#         return user_schema.dump(user)
#
#     # Function to delete an user
#     @classmethod
#     def delete(cls, user_id):
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             return {'message': 'User not found!'}, 404
#         user.delete_from_db()
#         return {'message': 'User successfully deleted.'}, 200
