# import Marshmallow
from marshmallow import Schema, fields, validates, ValidationError


# Declare the Schema for Item, which consists of item id, its name
# and description, the id of the category that it belongs to,
# and the id of the user who created it
class ItemSchema(Schema):
    # id of the item
    id = fields.Integer()
    # name of the item, it is required
    name = fields.String(required=True)
    # description of the item, not required
    description = fields.String(required=False)
    # id of the category item belongs to, it is required
    category_id = fields.Integer(required=True)
    # id of the creator of the item
    user_id = fields.Integer()

    # Function to validate the name of the item
    @validates("name")
    def validate_name(self, value):
        # Item's name must be a string with length in range [1,49]
        if type(value) != str:
            raise ValidationError("Item name must be a string.")
        if len(value) < 1:
            raise ValidationError("Length of Item name must be > 0.")
        if len(value) > 49:
            raise ValidationError("Length of Item name must be < 50.")

    # Function to validate the description of the item
    @validates("description")
    def validate_description(self, value):
        # The description must be a string
        if type(value) != str:
            raise ValidationError("Description must be a string.")

    # Function to validate the id of the category the item belongs to
    @validates("category_id")
    def validate_category_id(self, value):
        # The id must be an integer
        if type(value) != int:
            raise ValidationError("Category id must be an integer.")
