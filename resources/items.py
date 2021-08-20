# resource from restful
from flask_restful import Resource
# needed jwt functions
from flask_jwt_extended import jwt_required, get_jwt_identity

# model for item
from models.items import ItemModel
# model for category
from models.categories import CategoryModel
# schema for item
from schemas.items import ItemSchemaPOST, ItemSchema, Pagination
# decorator for validating request
from utilities import validate
# custom errors
from errors import CategoryDoesNotExist, ItemDoesNotExist, \
    UserForbidden, ItemNameDuplicate


# /categories/<category_id>/items/<item_id> resource
class Item(Resource):
    # Function to get a specific item
    @classmethod
    def get(cls, category_id, item_id):
        if not CategoryModel.find_by_id(category_id):
            # return 404 if category is not found
            raise CategoryDoesNotExist()
        # find the item in the database
        item = ItemModel.find_by_id(item_id)
        if item is None or item.category_id != category_id:
            # return 404 if category is not found
            raise ItemDoesNotExist()
        # if item is found, return info of the item
        return ItemSchema().dump(item)

    # Function to delete an item, jwt is required
    @jwt_required()
    def delete(self, category_id, item_id):
        if not CategoryModel.find_by_id(category_id):
            # return 404 if item's category not found
            raise CategoryDoesNotExist()

        # find the item in the database
        item = ItemModel.find_by_id(item_id)
        if item is None or item.category_id != category_id:
            # return 404 if item itself is not found
            raise ItemDoesNotExist()

        # if the requesting user is not creator of item
        if item.user_id != get_jwt_identity():
            # return 403 forbidden
            raise UserForbidden()
            # if user is creator, then delete the item
        item.delete_from_db()
        # return success message
        return {'message': 'Item deleted successfully'}

    # Function to edit an item, jwt is required
    @jwt_required()
    @validate(ItemSchema())
    def put(self, data, category_id, item_id):
        if not CategoryModel.find_by_id(category_id):
            # return 404 if item's category not found
            raise CategoryDoesNotExist()

        # find the item in the database
        item = ItemModel.find_by_id(item_id)
        if item is None or item.category_id != category_id:
            # return 404 if item itself is not found
            raise ItemDoesNotExist()

        if data['category_id'] != category_id:
            if ItemModel.find_by_category_and_name(data['category_id'],
                                                   data['name']):
                raise ItemNameDuplicate()

        # check if the requesting user is the item creator, if not return 403
        if item.user_id != get_jwt_identity():
            raise UserForbidden()

        # user is the item creator, modify items according to the request
        item.name = data['name']
        item.description = data['description']
        item.category_id = data['category_id']

        item.save_to_db()         # save changes to database

        return ItemSchema().dump(item)      # return info of changed item


# /categories/<category_id>/items resource
class CategoryItems(Resource):
    # Function to get all of the items within a category
    @classmethod
    def get(cls, category_id):
        # find the category in database
        category = CategoryModel.find_by_id(category_id)
        if category is None:
            # if category is not found, return 404
            raise CategoryDoesNotExist()
        # get the items list of the category
        items_list = category.items
        # return the list of info of the items
        return ItemSchema(many=True).dump(items_list)

    # Function to create a new item, user needs to login to do so
    @jwt_required()
    @validate(ItemSchemaPOST())
    def post(self, data, category_id):
        category = CategoryModel.find_by_id(category_id)
        # return 404 if item's category not found
        if not category:
            raise CategoryDoesNotExist()
        # return 400 ì item name already exists in given category
        if ItemModel.find_by_category_and_name(category_id, data['name']):
            raise ItemNameDuplicate()

        item_name = data['name']
        item_desc = data.get('description', '')
        # create an item with the data
        item = ItemModel(item_name, item_desc, category_id, get_jwt_identity())
        # save the created item to database
        item.save_to_db()
        # return the info of the created item
        return ItemSchema().dump(item), 201


# /items resource, in this case only used to
# get the latest (recently-added) items
class AllItems(Resource):
    @classmethod
    @validate(Pagination())
    def get(cls, data):
        # variables from arguments
        order = data['order']
        limit = int(data['limit'])
        page = int(data['page'])

        offset = limit * (page - 1)

        # get the items needed
        all_items = ItemSchema(many=True).dump(ItemModel.find_all(limit,
                                                                  offset,
                                                                  order))
        return {'items': all_items, 'total_items': len(all_items)}
