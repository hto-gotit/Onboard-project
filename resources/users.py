# resource and errors handling from restful
from flask_restful import Resource, abort

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
            abort(400, description='Username already exists')

        # username available, create a new user
        user = UserModel(data['username'], data['password'])
        # save the user to the database
        user.save_to_db()        

        return {'message': 'User created successfully'}, 201
