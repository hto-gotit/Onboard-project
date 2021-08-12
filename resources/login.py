from flask import request                               # import flask request
from flask_jwt_extended import create_access_token      # import needed jwt functions
from flask_restful import Resource                      # import resource from restful
import bcrypt                                           # import bcrypt for security use

from models.users import UserModel                      # import user models


# /auth/login resource
class UserLogin(Resource):
    # Function to log the user in
    @classmethod
    def post(cls):
        data = request.json                                         # fetch the request data
        if 'username' not in data:                                  # return 400 if the request does not have
            return {'message': 'Lacking field username'}, 400       # username key
        user = UserModel.find_by_username(data['username'])         # get the user from database
        if not user:
            return {'message': 'Invalid username'}, 400             # return 400 if username is invalid
        if user and verify_password(data['password'], user.password):     # if user exists and password is correct,
            try:                                                          # then return a jwt access token
                access_token = create_access_token(identity=user.id, fresh=True)
                return {'access_token': access_token}, 200
            except:
                return {'message': 'Internal error, login unsuccessful'}
        return {'message': 'Invalid password'}, 400                      # Otherwise, password is wrong


# Function to verify user request password for login and hashed password in the database
def verify_password(password, database_hash):
    pass_bytes = password.encode()                      # encode the request password
    hash_bytes = database_hash.encode()                 # encode the database hashed password
    return bcrypt.checkpw(pass_bytes, hash_bytes)       # return true if they are the same, false otherwise
