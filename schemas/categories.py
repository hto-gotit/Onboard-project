from marshmallow import Schema, fields, validates, ValidationError     # import Marshmallow


class CategorySchema(Schema):
    name = fields.String(required=True)

    @validates("name")
    def validate_username(self, value):
        if type(value) != str:
            raise ValidationError("Category name must be a string.")
        if len(value) < 1:
            raise ValidationError("Category name's length must be greater than 0.")
        if len(value) > 19:
            raise ValidationError("Category name's length must be less than 20.")
