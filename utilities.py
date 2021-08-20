# security
import bcrypt
# flask request
from flask import request
# class to raise error from validation in marshmallow
from marshmallow import ValidationError

# custom errors
from errors import ValidateSchemaError


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
def validate(schema):
    def validate_inner_func(func):
        def wrapper(requests, *args, **kwargs):
            # take body and args of the request
            data = {}
            if request.json:
                data.update(request.json)
            data.update(request.args)
            # validate the given data
            try:
                data = schema.load(data)
            except ValidationError:
                raise ValidateSchemaError()
            return func(requests, data, *args, **kwargs)
        return wrapper
    return validate_inner_func
