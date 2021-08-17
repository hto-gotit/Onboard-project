# needed jwt functions
from flask_jwt_extended import create_access_token
# resource from restful
from flask_restful import Resource

# user model
from models.users import UserModel
# function for verifying given password and decorator for validating request
from utilities import verify_password, user_request_validate


# /auth/login resource
class UserLogin(Resource):
    # Function to log the user in
    @classmethod
    @user_request_validate
    def post(cls, data):
        # get the user from database
        user = UserModel.find_by_username(data['username'])
        if user and verify_password(data['password'], user.password):
            # if user exists and password is correct, then
            # return a jwt token
            access_token = create_access_token(identity=user.id,
                                               fresh=True)
            return {'access_token': access_token}, 200
        # Otherwise, password is wrong
        return {'message': 'Invalid username or password'}, 400
