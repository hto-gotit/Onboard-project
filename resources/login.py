# import flask request
from flask import request
# import needed jwt functions
from flask_jwt_extended import create_access_token
# import resource from restful
from flask_restful import Resource
# import bcrypt for security use
import bcrypt

from models.users import UserModel            # import user models


# /auth/login resource
class UserLogin(Resource):
    # Function to log the user in
    @classmethod
    def post(cls):
        data = request.json       # fetch the request data
        if 'username' not in data:
            # return 400 if the request does not have username key
            return {'message': 'Lacking field username'}, 400
        # get the user from database
        user = UserModel.find_by_username(data['username'])
        if not user:
            # return 400 if username is invalid
            return {'message': 'Invalid username'}, 400
        try:
            if user and verify_password(data['password'], user.password):
                # if user exists and password is correct, then
                # return a jwt token
                try:
                    access_token = create_access_token(identity=user.id,
                                                       fresh=True)
                    return {'access_token': access_token}, 200
                except:
                    return {'message': 'Login unsuccessful'}, 500
            # Otherwise, password is wrong
        except ValueError:
            return {'message': 'Invalid password'}, 400
        return {'message': 'Invalid password'}, 400


# Function to verify user request password for login
# and hashed password in the database
def verify_password(password, database_hash):
    # encode the request password
    pass_bytes = password.encode()
    # encode the database hashed password
    hash_bytes = database_hash.encode()
    # return true if they are the same, false otherwise
    return bcrypt.checkpw(pass_bytes, hash_bytes)
