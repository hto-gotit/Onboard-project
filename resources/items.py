# import flask request
from flask import request
# import resource from restful
from flask_restful import Resource
# import needed jwt functions
from flask_jwt_extended import jwt_required, get_jwt_identity
# import class to raise errors for marshmallow
from marshmallow import ValidationError

# import model for item
from models.items import ItemModel
# import model for category
from models.categories import CategoryModel
# import schema for item
from schemas.items import ItemSchema


# /categories/<category_id>/items/<item_id> resource
class Item(Resource):
    # Function to get a specific item
    @classmethod
    def get(cls, category_id, item_id):
        # find the item in the database
        item = ItemModel.find_by_id(item_id)
        # declare schema for item
        item_schema = ItemSchema()
        if item is None:
            # if item not found, return 404
            return {'message': 'Item does not exists'}, 404
        try:
            # if item is found, return info of the item
            return item_schema.dump(item), 200
        except:
            return {'message': 'Internal error, cannot get item'}, 500

    # Function to delete an item, jwt is required
    @jwt_required()
    def delete(self, category_id, item_id):
        # fetch the person requesting the resource
        user_id = get_jwt_identity()
        # find the item in the database
        item = ItemModel.find_by_id(item_id)
        if item:                                            # if item is found
            # if the requesting user is not creator of item
            if item.user_id != user_id:
                return {'message': 'not creator'}, 403      # return forbidden

            try:
                # if user is creator, then delete the item
                item.delete_from_db()
            except:
                return {'message': 'Internal error, item was not deleted'}, 500
            # return success message
            return {'message': 'Item deleted'}, 200
        # if item not found, nothing needs to be deleted
        return {'message': 'Item does not exist'}, 200

    # Function to edit an item, jwt is required
    @jwt_required()
    def put(self, category_id, item_id):
        # fetch the person requesting the resource
        user_id = get_jwt_identity()
        # find the item in the database
        item = ItemModel.find_by_id(item_id)
        # get the info of the request
        data = request.json
        # declare the schema for item
        item_schema = ItemSchema()

        # validate the request
        try:
            item_schema.load(data)
        except ValidationError as err:
            return err.messages

        if not CategoryModel.find_by_id(data['category_id']):
            # return 404 if item's category not found
            return {'message': 'There is no such category'}, 400

        if item is None:
            # return 404 if item itself is not found
            return {'message': 'Item does not exist'}, 404

        # check if the requesting user is the item creator, if not return 403
        if user_id != item.user_id:
            return {'message': 'Not item creator, cannot edit item'}, 403
        else:
            # user is the item creator, modify items according to the request
            item.name = data['name']
            item.description = data['description']
            item.category_id = data['category_id']

        try:
            item.save_to_db()         # save changes to database
        except:
            return{'message': 'Internal error, item was not saved'}, 500

        return item_schema.dump(item), 200     # return info of changed item


# /categories/<category_id>/items resource
class ItemList(Resource):
    # Function to get all of the items within a category
    @classmethod
    def get(cls, category_id):
        # find the category in database
        category = CategoryModel.find_by_id(category_id)
        if category is None:
            # if category is not found, return 404
            return {'message': 'Category not found'}, 404
        # get the items list of the category
        items_list = category.items
        # declare schemas for the items
        items_list_schema = ItemSchema(many=True)
        try:
            # return the list of info of the items
            return items_list_schema.dump(items_list), 200
        except:
            return {'message': 'Internal error, cannot get items list'}, 500

    # Function to create a new item, user needs to login to do so
    @jwt_required()
    def post(self, category_id):
        user_id = get_jwt_identity()       # Get the id of the requesting user
        data = request.json                # Get the info of the request
        item_schema = ItemSchema()         # Declare the schema for item

        try:
            item_schema.load(data)              # validate the request info
        except ValidationError as err:
            return err.messages
        # if category is not found, return 404
        if not CategoryModel.find_by_id(data['category_id']):
            return {'message': 'There is no such category'}, 400

        data['user_id'] = user_id          # append the user's id to the data
        item = ItemModel(**data)           # create an item with the data

        try:
            item.save_to_db()              # save the created item to database
        except:
            return {'message': 'an error occured when inserting the item.'}, 500
        # return the info of the created item
        return item_schema.dump(item), 201


# /items resource, in this case only used to
# get the latest (recently-added) items
class ItemLatests(Resource):
    @classmethod
    def get(cls):
        # get the parameters
        args = request.args
        # declare schemas for the items
        item_latest_schema = ItemSchema(many=True)
        # fetch all of the items from database
        all_items = item_latest_schema.dump(ItemModel.find_all())
        if args['order'] == 'desc':
            # returned list is ordered from later to earlier
            try:
                # if there are more allowed items to show than
                # items in database, show all items
                if len(all_items) <= int(args['limit']):
                    return all_items[::-1], 200
                else:
                    # else only show the "limit" amount of items
                    all_items = all_items[len(all_items)-int(args['limit']):
                                          len(all_items)]
                    return all_items[::-1], 200
            except:
                return {'message': 'Cannot get latest items list'}, 500
        elif args['order'] == 'asc':
            # returned list is ordered from earlier to later
            try:
                if len(all_items) <= int(args['limit']):
                    return all_items, 200
                else:
                    all_items = all_items[len(all_items)-int(args['limit']):
                                          len(all_items)]
                    return all_items, 200
            except:
                return {'message': 'Cannot get latest items list'}, 500
        else:
            # return 400 otherwise
            return {'message': 'Order parameter not recognized'}, 400
