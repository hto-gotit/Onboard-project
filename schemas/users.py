from marshmallow import Schema, fields, ValidationError, validates     # import Marshmallow


class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates("username")
    def validate_username(self, value):
        if type(value) != str:
            raise ValidationError("Username must be a string.")
        if len(value) < 1:
            raise ValidationError("Username's length must be greater than 0.")
        if len(value) > 79:
            raise ValidationError("Username's length must be less than 80.")

    @validates("password")
    def validate_password(self, value):
        if type(value) != str:
            raise ValidationError("Password must be a string.")
        if len(value) < 1:
            raise ValidationError("Password's length must be greater than 0.")
        if len(value) > 79:
            raise ValidationError("Password's length must be less than 80.")
