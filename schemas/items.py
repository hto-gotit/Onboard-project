# import Marshmallow
from marshmallow import Schema, fields, validates, ValidationError


# Declare the Schema for Item for method POST, which consists of item id,
# its name and description and the id of the user who created it
class ItemSchemaPOST(Schema):
    # id of the item
    id = fields.Integer()
    # name of the item, it is required
    name = fields.String(required=True)
    # description of the item, not required
    description = fields.String(required=False)

    # id of the creator of the item
    user_id = fields.Integer()

    # Function to validate the name of the item
    @validates('name')
    def validate_name(self, value):
        # Item's name must be a string with length in range [1,49]
        if len(value) < 1:
            raise ValidationError('Length of Item name must be > 0.')
        if len(value) > 49:
            raise ValidationError('Length of Item name must be < 50.')
        if value[0] == ' ' or value[-1] == ' ':
            raise ValidationError('Item name cannot have space in the '
                                  'beginning and the end')


# Declare the (full) Schema for Item, which extends the schema for item with
# method POST. This schema adds another field which is category_id (the id
# of the category the item belongs to)
class ItemSchema(ItemSchemaPOST):
    # id of the category item belongs to, it is required
    category_id = fields.Integer(required=True)

    # Validate the category_id of item
    @validates('category_id')
    def validate_name(self, value):
        # Item's category_id must be positive
        if value < 1:
            raise ValidationError('Category_id cannot be negative')


# Declare the Schema for arguments for finding latest Items, which consists of
# limit, page, and order. Limit is the number of items in a page. Page is the
# page number to get. Order is the ordering by item id to fetch from database.
class Pagination(Schema):
    # number of items per page
    limit = fields.Integer(required=True)
    # page number to get from
    page = fields.Integer(required=True)
    # ordering of the list to get from database
    order = fields.String(required=True)

    # Validate limit argument
    @validates('limit')
    def validate_limit(self, value):
        # limit can only be positive
        if value < 1:
            raise ValidationError('Limit must be > 0.')

    # Validate page argument
    @validates('page')
    def validate_page(self, value):
        # page can only be positive
        if value < 1:
            raise ValidationError('Page must be > 0.')

    # Validate order argument
    @validates('order')
    def validate_order(self, value):
        # order can only be either asc or desc
        if value != 'asc' and value != 'desc':
            raise ValidationError('Order can only take values asc or desc')
