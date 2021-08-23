# import Marshmallow
from marshmallow import Schema, fields, validate
# import constants
from config.constants import *


# Declare the Schema for Category, which consists of category id and its name
class CategorySchema(Schema):
    # id of the category
    id = fields.Integer()
    # name of the category, it is required
    name = fields.String(required=True,
                         validate=validate.Length(
                             min=min_string_length,
                             max=max_category_name_length)
                         )
