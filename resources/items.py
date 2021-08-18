# resource and errors handling from restful
from flask import request, abort
# resource from restful
from flask_restful import Resource
# needed jwt functions
from flask_jwt_extended import jwt_required, get_jwt_identity

# model for item
from models.items import ItemModel
# model for category
from models.categories import CategoryModel
# schema for item
from schemas.items import ItemSchema
# decorator for validating request
from utilities import item_request_validate_put, item_request_validate_post


# /categories/<category_id>/items/<item_id> resource
class Item(Resource):
    # Function to get a specific item
    @classmethod
    def get(cls, category_id, item_id):
        if not CategoryModel.find_by_id(category_id):
            # return 404 if category is not found
            abort(404)
        # find the item in the database
        item = ItemModel.find_by_id(item_id)
        if item is None or item.category_id != category_id:
            # return 404 if category is not found
            abort(404)
        # declare schema for item
        item_schema = ItemSchema()
        # if item is found, return info of the item
        return item_schema.dump(item), 200

    # Function to delete an item, jwt is required
    @jwt_required()
    def delete(self, category_id, item_id):
        if not CategoryModel.find_by_id(category_id):
            # return 404 if item's category not found
            abort(404)

        # find the item in the database
        item = ItemModel.find_by_id(item_id)
        if item is None or item.category_id != category_id:
            # return 404 if item itself is not found
            abort(404)

        # fetch the person requesting the resource
        user_id = get_jwt_identity()

        # if the requesting user is not creator of item
        if item.user_id != user_id:
            # return forbidden
            abort(403)
            # if user is creator, then delete the item
        item.delete_from_db()
        # return success message
        return {'message': 'Item deleted'}, 200

    # Function to edit an item, jwt is required
    @jwt_required()
    @item_request_validate_put
    def put(self, category_id, item_id, data, item_schema):
        if not CategoryModel.find_by_id(category_id):
            # return 404 if item's category not found
            abort(404)

        # find the item in the database
        item = ItemModel.find_by_id(item_id)
        if item is None or item.category_id != category_id:
            # return 404 if item itself is not found
            abort(404)

        # fetch the person requesting the resource
        user_id = get_jwt_identity()

        if data['category_id'] != category_id:
            if ItemModel.find_by_category_and_name(data['category_id'],
                                                   data['name']):
                abort(400, description='Item name already exists '
                                       'in destination category')

        # check if the requesting user is the item creator, if not return 403
        if user_id != item.user_id:
            abort(403)
        else:
            # user is the item creator, modify items according to the request
            item.name = data['name']
            item.description = data['description']
            item.category_id = data['category_id']

        item.save_to_db()         # save changes to database

        return item_schema.dump(item)      # return info of changed item


# /categories/<category_id>/items resource
class CategoryItems(Resource):
    # Function to get all of the items within a category
    @classmethod
    def get(cls, category_id):
        # find the category in database
        category = CategoryModel.find_by_id(category_id)
        if category is None:
            # if category is not found, return 404
            abort(404)
        # get the items list of the category
        items_list = category.items
        # declare schemas for the items
        items_list_schema = ItemSchema(many=True)
        # return the list of info of the items
        return items_list_schema.dump(items_list)

    # Function to create a new item, user needs to login to do so
    @jwt_required()
    @item_request_validate_post
    def post(self, category_id, data, item_schema):
        category = CategoryModel.find_by_id(category_id)
        if not category:
            abort(404)
        user_id = get_jwt_identity()       # Get the id of the requesting user
        if ItemModel.find_by_category_and_name(category_id, data['name']):
            abort(400, description='Item name already exists in this category')
            
        item_name = data['name']
        if 'description' in data:
            item_desc = data['description']
        else:
            item_desc = ''
        # create an item with the data
        item = ItemModel(item_name, item_desc, category_id, user_id)

        item.save_to_db()              # save the created item to database
        # return the info of the created item
        return item_schema.dump(item), 201


# /items resource, in this case only used to
# get the latest (recently-added) items
class AllItems(Resource):
    @classmethod
    def get(cls):
        # get the parameters
        args = request.args
        # declare schemas for the items
        item_latest_schema = ItemSchema(many=True)
        if args['order'] == 'desc' or args['order'] == 'asc':
            limit = int(args['limit'])
            page = int(args['page'])
            if limit < 0 or page < 0:
                abort(400, description='limit and page must be positive')
            order = args['order']
            pages_list = []
            for i in range(page):
                skip = limit*i
                all_items = item_latest_schema.dump(ItemModel.find_all(limit,
                                                                       skip,
                                                                       order))
                if not all_items:
                    break
                pages_list.append({'items': all_items,
                                   'total_items': len(all_items)})
            return pages_list
        else:
            # return 400 otherwise
            abort(400, description='Order parameter not recognized')
