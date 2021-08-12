from flask_restful import Resource
from models.categories import CategoryModel
from schemas.categories import CategorySchema


class CategoryList(Resource):
    def get(self):
        category_list_schema = CategorySchema(many=True)
        try:
            return category_list_schema.dump(CategoryModel.find_all()), 200
        except:
            return {'message': 'Cannot get categories list, internal error'}, 500


# class Category(Resource):
#     def get(self, category_id):
#         category = CategoryModel.find_by_id(category_id)
#         category_schema = CategorySchema()
#
#         if category:
#             return category.json()
#         return {'message': 'Category not found'}, 404
#
#     def post(self, category_id):
#         if CategoryModel.find_by_id(category_id):
#             return {'message' : "Category '{}' already exists".format(category_id)}, 400
#         category = CategoryModel('CatNo' + str(category_id))
#         # try:
#         category.save_to_db()
#         # except:
#         #     return {'message' : 'Error creating category'}, 500
#         return category.json(), 201
#
#     def delete(self, category_id):
#         category = CategoryModel.find_by_id(category_id)
#         if category:
#             category.delete_from_db()
#         return {'message': 'Category deleted'}
