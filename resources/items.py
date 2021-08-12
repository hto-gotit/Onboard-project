from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from models.items import ItemModel
from models.categories import CategoryModel
from schemas.items import ItemSchema


class Item(Resource):
    def get(self, category_id, item_id):
        item = ItemModel.find_by_id(item_id)
        item_schema = ItemSchema()
        if item is None:
            return {'message': 'Item does not exists'}, 404
        try:
            return item_schema.dump(item)
        except:
            return {'message': 'Internal error, cannot get item'}, 500

    @jwt_required()
    def delete(self, category_id, item_id):
        user_id = get_jwt_identity()
        item = ItemModel.find_by_id(item_id)
        if item:
            if item.user_id != user_id:
                return {'message': 'not creator'}, 403
            if item:
                try:
                    item.delete_from_db()
                except:
                    return {'message': 'Internal error, item was not deleted'}, 500
            return {'message': 'Item deleted'}, 200
        return {'message': 'Item does not exist'}, 200

    @jwt_required()
    def put(self, category_id, item_id):
        user_id = get_jwt_identity()
        item = ItemModel.find_by_id(item_id)
        data = request.json
        item_schema = ItemSchema()

        try:
            item_schema.load(data)
        except ValidationError as err:
            return err.messages

        if not CategoryModel.find_by_id(data['category_id']):
            return {'message': 'There is no such category'}, 400

        if item is None:
            return {'mes': 'Item does not exist'}, 404
        if user_id != item.user_id:
            return {'message': 'Not item creator, cannot edit item'}, 403
        else:
            item.name = data['name']
            item.description = data['description']
            item.category_id = data['category_id']

        try:
            item.save_to_db()
        except:
            return{'message': 'Internal error, item was not saved'}, 500

        return item_schema.dump(item), 200


class ItemList(Resource):
    def get(self, category_id):
        category = CategoryModel.find_by_id(category_id)
        if category is None:
            return {'message': 'Category not found'}, 404
        items_list = category.items
        items_list_schema = ItemSchema(many=True)
        try:
            return items_list_schema.dump(items_list)
        except:
            return {'message': 'Internal error, cannot get items list'}, 500


class ItemCreate(Resource):
    @jwt_required()
    def post(self, category_id):
        user_id = get_jwt_identity()
        data = request.json
        item_schema = ItemSchema()

        try:
            item_schema.load(data)
        except ValidationError as err:
            return err.messages

        if not CategoryModel.find_by_id(data['category_id']):
            return {'message': 'There is no such category'}, 400

        data['user_id'] = user_id
        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {'message': 'an error occured when inserting the item.'}, 500

        return item_schema.dump(item), 201

