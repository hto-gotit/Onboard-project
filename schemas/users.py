from marshmallow import Schema, fields, ValidationError, validates     # import Marshmallow


# Declare the Schema for User, which consists of user's username and password
class UserSchema(Schema):
    username = fields.String(required=True)         # username of the account
    password = fields.String(required=True)         # password of the account

    # Function to validate the username of the account
    @validates("username")
    def validate_username(self, value):
        if type(value) != str:
            raise ValidationError("Username must be a string.")                   # The username must be a string
        if len(value) < 1:                                                        # with length in range [1,79]
            raise ValidationError("Username's length must be greater than 0.")
        if len(value) > 79:
            raise ValidationError("Username's length must be less than 80.")

    # Function to validate the password of the account
    @validates("password")
    def validate_password(self, value):
        if type(value) != str:
            raise ValidationError("Password must be a string.")                    # The password must be a string
        if len(value) < 1:                                                         # with length in range [1,79]
            raise ValidationError("Password's length must be greater than 0.")
        if len(value) > 79:
            raise ValidationError("Password's length must be less than 80.")
