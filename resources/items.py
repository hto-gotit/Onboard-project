from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.items import ItemModel, ItemSchema


class Item(Resource):
    parser = reqparse.RequestParser()

    def get(self, item_id):
        item = ItemModel.find_by_id(item_id)
        item_schema = ItemSchema()
        if item:
            return item_schema.dump(item), 200
        return {'message' : 'Item does not exists' }, 404


    @jwt_required
    def put(self, item_id):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_id(item_id)
        item_schema = ItemSchema()
        item.name = data['name']
        item.description = data['description']
        item.category_id = data['category_id']
        item.save_to_db
        return item_schema.dump(item), 200

    @jwt_required
    def delete(self, item_id):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_id(item_id)
        item.delete_from_db
        return {'message': 'Item deleted successfully'}


class CreateItem(Resource):
    @jwt_required
    def post(self):
        data = CategoryItems.parser.parse_args()
        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {'message': 'Internal error, item was not created.'}, 500

        return item.dump(), 400

