# resource from restful
from flask_restful import Resource

# model for user
from models.users import UserModel
# decorator for validating request
from utilities import user_request_validate


# /users resource, used only for registering a new user
class UserRegister(Resource):
    # Function to create a new user
    @classmethod
    @user_request_validate
    def post(cls, data):
        if UserModel.find_by_username(data['username']):
            # if username already existed, return 400
            return {'message': 'Username already exists'}, 400

        # username available, create a new user
        user = UserModel(data['username'], data['password'])
        user.save_to_db()        # save the user to the database

        return {'message': 'User created successfully'}, 201


# /user/user_id resource (Not available to users)
# class User(Resource):
#     # Function to get id and username of an user
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
