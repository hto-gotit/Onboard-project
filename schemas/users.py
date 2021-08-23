# import Marshmallow
from marshmallow import Schema, fields, validate, pre_load
# import constants
from config.constants import *


# Declare the Schema for User, which consists of user's username and password
class UserSchema(Schema):
    # username of the account
    username = fields.String(required=True,
                             validate=validate.Length(
                                 min=min_string_length,
                                 max=max_user_string_length)
                             )

    # password of the account
    password = fields.String(required=True,
                             validate=validate.Length(
                                 min=min_string_length,
                                 max=max_user_string_length)
                             )

    @pre_load
    def strip_whitespace(self, in_data, **kwargs):
        if all(key in in_data and type(in_data[key]) == str
               for key in ('username', 'password')):
            in_data['username'] = in_data['username'].strip()
            in_data['password'] = in_data['password'].strip()
        return in_data
