# security
import bcrypt
# flask request
from flask import request
# class to raise error from validation in marshmallow
from marshmallow import ValidationError
# schema for user
from schemas.users import UserSchema
# schema for item
from schemas.items import ItemSchema


# Function to hash a given password, using bcrypt hash functions
def bcrypt_hash(password):
    # Encode the raw password
    pass_bytes = password.encode()
    # Hash the encoded and use a generated salt
    pass_hash_bytes = bcrypt.hashpw(pass_bytes, bcrypt.gensalt(14))
    # return hashed password
    return pass_hash_bytes.decode()


# Function to verify user request password for login
# and hashed password in the database
def verify_password(password, database_hash):
    # encode the request password
    pass_bytes = password.encode()
    # encode the database hashed password
    hash_bytes = database_hash.encode()
    # return true if they are the same, false otherwise
    return bcrypt.checkpw(pass_bytes, hash_bytes)


# Decorator for taking and validating request for users
def user_request_validate(f):
    def g(requests, *args, **kwargs):
        # take body of the request
        data = request.json
        # declare the schema for user
        user_schema = UserSchema()
        # validate the request
        try:
            data = user_schema.load(data)
        except ValidationError as err:
            return err.messages
        return f(requests, data)
    return g


# Decorator for taking and validating request for items
def item_request_validate(f):
    def g(requests, *args, **kwargs):
        # take the method of the request
        method = request.method
        # take the body of the request
        data = request.json
        # declare the schema for item
        item_schema = ItemSchema()
        # take the category_id from url
        category_id = kwargs['category_id']
        if method == 'POST':
            # append category_id to body if creating new item
            data['category_id'] = category_id
        # validate the request
        try:
            data = item_schema.load(data)
        except ValidationError as err:
            return err.messages
        if method == 'PUT':
            # take item_id if editing an item
            item_id = kwargs['item_id']
            return f(requests, category_id, item_id, data, item_schema)
        elif method == 'POST':
            return f(requests, category_id, data, item_schema)
    return g

