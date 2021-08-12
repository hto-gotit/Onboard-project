from marshmallow import Schema, fields, validates, ValidationError     # import Marshmallow


class ItemSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=False)
    category_id = fields.Integer(required=True)

    @validates("name")
    def validate_name(self, value):
        if type(value) != str:
            raise ValidationError("Item name must be a string.")
        if len(value) < 1:
            raise ValidationError("Length of Item name must be greater than 0.")
        if len(value) > 49:
            raise ValidationError("Length of Item name must be less than 50.")

    @validates("description")
    def validate_description(self, value):
        if type(value) != str:
            raise ValidationError("Description must be a string.")

    @validates("category_id")
    def validate_category_id(self, value):
        if type(value) != int:
            raise ValidationError("Category id must be an integer.")
