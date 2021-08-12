from marshmallow import Schema, fields, validates, ValidationError     # import Marshmallow


# Declare the Schema for Category, which consists of category id and its name
class CategorySchema(Schema):
    id = fields.Integer()                       # id of the category
    name = fields.String(required=True)         # name of the category, it is required

    # function to validate the name of the category
    @validates("name")
    def validate_username(self, value):
        if type(value) != str:                                                       # name must be a string
            raise ValidationError("Category name must be a string.")
        if len(value) < 1:                                                           # name length must be in the
            raise ValidationError("Category name's length must be greater than 0.")  # range of [1,19]
        if len(value) > 19:
            raise ValidationError("Category name's length must be less than 20.")
