# resource from restful
from flask_restful import Resource

# model of category
from models.categories import CategoryModel
# schema of category
from schemas.categories import CategorySchema


# /categories resource
class CategoryList(Resource):
    # Function to get all of the available categories
    @classmethod
    def get(cls):
        # declare the Schemas of categories
        category_list_schema = CategorySchema(many=True)
        # try getting all categories
        return category_list_schema.dump(CategoryModel.find_all())
