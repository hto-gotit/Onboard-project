from flask_restful import Resource, reqparse
from models.categories import CategoryModel, CategorySchema


class CategoryItems(Resource):
    parser = reqparse.RequestParser()

    def get(self, category_id):
        category = CategoryModel.find_by_id(category_id)
        category_schema = CategorySchema()
        if category:
            return category_schema.dump(category)
        return {'message': 'Store not found'}, 404


class CategoriesList(Resource):
    def get(self, category_id):
        category = CategoryModel.find_by_name(category_id)
        category_schema = CategorySchema()
        if category:
            return category_schema.dump(category)
        return {'message': 'Store not found'}, 404
