from flask_restful import Resource              # import resource from restful

from models.categories import CategoryModel     # import model of category
from schemas.categories import CategorySchema   # import schema of category


# /categories resource
class CategoryList(Resource):
    # Function to get all of the available categories
    @classmethod
    def get(cls):
        # declare the Schemas of categories
        category_list_schema = CategorySchema(many=True)
        # try getting all categories
        try:
            return category_list_schema.dump(CategoryModel.find_all()), 200
        except:
            return {'message': 'Cannot get categories list'}, 500


# /categories/<category_id> resource (not available to users)
# class Category(Resource):
#     # Function to get the information of a specified category
#     @classmethod
#     def get(cls, category_id):
#         category = CategoryModel.find_by_id(category_id)
#         category_schema = CategorySchema()
#
#         if category:
#             return category_schema.dump(category), 200
#         return {'message': 'Category not found'}, 404
#
#     # Function to create a category
#     @classmethod
#     def post(cls, category_id):
#         if CategoryModel.find_by_id(category_id):
#             return {'message' :
#             "Category '{}' already exists".format(category_id)}, 400
#         category = CategoryModel('CatNo' + str(category_id))
#         category_schema = CategorySchema()
#
#         try:
#             category.save_to_db()
#         except:
#             return {'message' : 'Error creating category'}, 500
#
#         return category_schema.dump(category), 201
#
#     # Function to delete a category
#     @classmethod
#     def delete(cls, category_id):
#         category = CategoryModel.find_by_id(category_id)
#         if category:
#             category.delete_from_db()
#         return {'message': 'Category deleted'}
from flask_restful import Resource              # import resource from restful

from models.categories import CategoryModel     # import model of category
from schemas.categories import CategorySchema   # import schema of category


# /categories resource
class CategoryList(Resource):
    # Function to get all of the available categories
    @classmethod
    def get(cls):
        # declare the Schemas of categories
        category_list_schema = CategorySchema(many=True)
        # try getting all categories
        try:
            return category_list_schema.dump(CategoryModel.find_all()), 200
        except:
            return {'message': 'Cannot get categories list'}, 500


# /categories/<category_id> resource (not available to users)
# class Category(Resource):
#     # Function to get the information of a specified category
#     @classmethod
#     def get(cls, category_id):
#         category = CategoryModel.find_by_id(category_id)
#         category_schema = CategorySchema()
#
#         if category:
#             return category_schema.dump(category), 200
#         return {'message': 'Category not found'}, 404
#
#     # Function to create a category
#     @classmethod
#     def post(cls, category_id):
#         if CategoryModel.find_by_id(category_id):
#             return {'message' :
#             "Category '{}' already exists".format(category_id)}, 400
#         category = CategoryModel('CatNo' + str(category_id))
#         category_schema = CategorySchema()
#
#         try:
#             category.save_to_db()
#         except:
#             return {'message' : 'Error creating category'}, 500
#
#         return category_schema.dump(category), 201
#
#     # Function to delete a category
#     @classmethod
#     def delete(cls, category_id):
#         category = CategoryModel.find_by_id(category_id)
#         if category:
#             category.delete_from_db()
#         return {'message': 'Category deleted'}
