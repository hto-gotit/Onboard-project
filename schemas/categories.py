# import Marshmallow
from marshmallow import Schema, fields, validates, ValidationError


# Declare the Schema for Category, which consists of category id and its name
class CategorySchema(Schema):
    # id of the category
    id = fields.Integer()
    # name of the category, it is required
    name = fields.String(required=True)

    # function to validate the name of the category
    @validates("name")
    def validate_username(self, value):
        # name length must be in the range of [1,19]
        if len(value) < 1:
            raise ValidationError("Category name's length must be > 0.")
        if len(value) > 19:
            raise ValidationError("Category name's length must be < 20.")
