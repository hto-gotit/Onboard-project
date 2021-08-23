# import Marshmallow
from marshmallow import Schema, fields, validate, pre_load
# import constants
from config.constants import *


# Declare the Schema for Item for method POST, which consists of item id,
# its name and description and the id of the user who created it
class CreateItemSchema(Schema):
    # id of the item
    id = fields.Integer()
    # name of the item, it is required
    name = fields.String(required=True,
                         validate=validate.Length(min=min_string_length,
                                                  max=max_item_name_length))
    # description of the item, not required
    description = fields.String(required=False)
    # id of the creator of the item
    user_id = fields.Integer()

    # Function to validate the name of the item
    @pre_load
    def strip_whitespace(self, in_data, **kwargs):
        if 'name' in in_data and type(in_data['name']) == str:
            in_data['name'] = in_data['name'].strip()
        if 'description' in in_data and type(in_data['description']) == str:
            in_data['description'] = in_data['description'].strip()
        return in_data


# Declare the (full) Schema for Item, which extends the schema for item with
# method POST. This schema adds another field which is category_id (the id
# of the category the item belongs to)
class ItemSchema(CreateItemSchema):
    # id of the category item belongs to, it is required
    category_id = fields.Integer(required=True,
                                 validate=validate.Range(min=min_integer))


# Declare the Schema for arguments for finding latest Items, which consists of
# limit, page, and order. Limit is the number of items in a page. Page is the
# page number to get. Order is the ordering by item id to fetch from database.
class PaginationSchema(Schema):
    # number of items per page
    limit = fields.Integer(required=True,
                           validate=validate.Range(min=min_integer))
    # page number to get from
    page = fields.Integer(required=True,
                          validate=validate.Range(min=min_integer))
    # ordering of the list to get from database
    order = fields.String(required=True,
                          validate=validate.OneOf(['asc', 'desc']))
