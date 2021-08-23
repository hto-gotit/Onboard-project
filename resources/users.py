# resource and errors handling from restful
from flask_restful import Resource

# model for user
from models.user import UserModel
# user schema
from schemas.users import UserSchema
# decorator for validating request
from utilities import validate
# custom errors
from errors import UsernameAlreadyExists


# /users resource, used only for registering a new user
class UserRegister(Resource):
    # Function to create a new user
    @classmethod
    @validate(UserSchema())
    def post(cls, data):
        if UserModel.find_by_username(data['username']):
            raise UsernameAlreadyExists()

        # username available, create a new user
        user = UserModel(username=data['username'],
                         hash_password=data['password'])
        user.save_to_db()

        return {'message': 'User created successfully'}, 201
