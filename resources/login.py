# needed jwt functions
from flask_jwt_extended import create_access_token
# resource and errors handling from restful
from flask_restful import Resource

# user model
from models.user import UserModel
# user schema
from schemas.users import UserSchema
# function for verifying given password and decorator for validating request
from utilities import verify_password, validate
# custom errors
from errors import InvalidCredentials


# /auth/login resource
class UserLogin(Resource):
    # Function to log the user in
    @classmethod
    @validate(UserSchema())
    def post(cls, data):
        # get the user from database
        user = UserModel.find_by_username(data['username'])
        if user and verify_password(data['password'], user.password):
            # if user exists and password is correct, then
            # return a jwt token
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}
        # Otherwise, password is wrong
        raise InvalidCredentials()
