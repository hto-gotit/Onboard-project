# import Marshmallow
from marshmallow import Schema, fields, ValidationError, validates


# Declare the Schema for User, which consists of user's username and password
class UserSchema(Schema):
    username = fields.String(required=True)         # username of the account
    password = fields.String(required=True)         # password of the account

    # Function to validate the username of the account
    @validates("username")
    def validate_username(self, value):
        # The username must be a string with length in range [1,79]
        if type(value) != str:
            raise ValidationError("Username must be a string.")
        if len(value) < 1:
            raise ValidationError("Username's length must be > 0.")
        if len(value) > 79:
            raise ValidationError("Username's length must be < 80.")
        if value[0] == ' ' or value[-1] == ' ':
            raise ValidationError("Username cannot have empty space in the "
                                  "beginning and the end")

    # Function to validate the password of the account
    @validates("password")
    def validate_password(self, value):
        # The password must be a string with length in range [1,79]
        if type(value) != str:
            raise ValidationError("Password must be a string.")
        if len(value) < 1:
            raise ValidationError("Password's length must be > 0.")
        if len(value) > 79:
            raise ValidationError("Password's length must be < 80.")
        if value[0] == ' ' or value[-1] == ' ':
            raise ValidationError("Username cannot have space in the "
                                  "beginning and the end")
