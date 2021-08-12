from flask import request                                       # import flask request
from flask_restful import Resource                              # import resource from restful
from flask_jwt_extended import jwt_required, get_jwt_identity   # import needed jwt functions
from marshmallow import ValidationError                         # import class to raise errors for marshmallow

from models.items import ItemModel                              # import model for item
from models.categories import CategoryModel                     # import model for category
from schemas.items import ItemSchema                            # import schema for item


# /categories/<category_id>/items/<item_id> resource
class Item(Resource):
    # Function to get a specific item
    @classmethod
    def get(cls, category_id, item_id):
        item = ItemModel.find_by_id(item_id)                        # find the item in the database
        item_schema = ItemSchema()                                  # declare schema for item
        if item is None:
            return {'message': 'Item does not exists'}, 404         # if item not found, return 404
        try:
            return item_schema.dump(item)                           # if item is found, return info of the item
        except:
            return {'message': 'Internal error, cannot get item'}, 500

    # Function to delete an item, jwt is required
    @jwt_required()
    def delete(self, category_id, item_id):
        user_id = get_jwt_identity()                        # fetch the person requesting the resource
        item = ItemModel.find_by_id(item_id)                # find the item in the database
        if item:                                            # if item is found
            if item.user_id != user_id:                     # if the requesting user is not creator of item
                return {'message': 'not creator'}, 403      # return forbidden

            try:
                item.delete_from_db()                       # if user is creator, then delete the item
            except:
                return {'message': 'Internal error, item was not deleted'}, 500

            return {'message': 'Item deleted'}, 200         # return success message
        return {'message': 'Item does not exist'}, 200      # if item not found, nothing needs to be deleted

    # Function to edit an item, jwt is required
    @jwt_required()
    def put(self, category_id, item_id):
        user_id = get_jwt_identity()                        # fetch the person requesting the resource
        item = ItemModel.find_by_id(item_id)                # find the item in the database
        data = request.json                                 # get the info of the request
        item_schema = ItemSchema()                          # declare the schema for item

        try:
            item_schema.load(data)                          # validate the request
        except ValidationError as err:
            return err.messages

        if not CategoryModel.find_by_id(data['category_id']):
            return {'message': 'There is no such category'}, 400    # return 404 if item's category not found

        if item is None:
            return {'message': 'Item does not exist'}, 404          # return 404 if item itself is not found
        if user_id != item.user_id:                                          # check if the requesting user is the
            return {'message': 'Not item creator, cannot edit item'}, 403    # item creator, if not return 403
        else:
            item.name = data['name']                                # user is the item creator, modify
            item.description = data['description']                  # items according to the request
            item.category_id = data['category_id']

        try:
            item.save_to_db()                                       # save changes to database
        except:
            return{'message': 'Internal error, item was not saved'}, 500

        return item_schema.dump(item), 200                          # return info of changed item


# /categories/<category_id>/items resource
class ItemList(Resource):
    # Function to get all of the items within a category
    @classmethod
    def get(cls, category_id):
        category = CategoryModel.find_by_id(category_id)            # find the category in database
        if category is None:                                        # if category is not found, return 404
            return {'message': 'Category not found'}, 404
        items_list = category.items                                 # get the items list of the category
        items_list_schema = ItemSchema(many=True)                   # declare schemas for the items
        try:
            return items_list_schema.dump(items_list)               # return the list of info of the items
        except:
            return {'message': 'Internal error, cannot get items list'}, 500

    # Function to create a new item, user needs to login to do so
    @jwt_required()
    def post(self, category_id):
        user_id = get_jwt_identity()            # Get the id of the requesting user
        data = request.json                     # Get the info of the request
        item_schema = ItemSchema()              # Declare the schema for item

        try:
            item_schema.load(data)              # validate the request info
        except ValidationError as err:
            return err.messages

        if not CategoryModel.find_by_id(data['category_id']):           # if category is not found, return 404
            return {'message': 'There is no such category'}, 400

        data['user_id'] = user_id               # append the user's id to the data
        item = ItemModel(**data)                # create an item with the data

        try:
            item.save_to_db()                   # save the created item to database
        except:
            return {'message': 'an error occured when inserting the item.'}, 500

        return item_schema.dump(item), 201      # return the info of the created item


# /items resource, in this case only used to get the latest (recently-added) items
class ItemLatests(Resource):
    @classmethod
    def get(cls):
        args = request.args                                         # get the parameters
        item_latest_schema = ItemSchema(many=True)                  # declare schemas for the items
        all_items = item_latest_schema.dump(ItemModel.find_all())   # fetch all of the items from database
        if args['order'] == 'desc':                                 # returned list is ordered from later to earlier
            try:
                if len(all_items) <= int(args['limit']):            # if there are more allowed items to show than
                    return all_items[::-1], 200                     # items in database, show all items
                else:                                               # else only show the "limit" amount of items
                    all_items = all_items[len(all_items)-int(args['limit']):len(all_items)]
                    return all_items[::-1], 200
            except:
                return {'message': 'Cannot get latest items list, internal error'}, 500
        elif args['order'] == 'asc':                                # returned list is ordered from earlier to later
            try:
                if len(all_items) <= int(args['limit']):
                    return all_items, 200
                else:
                    all_items = all_items[len(all_items)-int(args['limit']):len(all_items)]
                    return all_items, 200
            except:
                return {'message': 'Cannot get latest items list, internal error'}, 500
        else:
            return {'message': 'Order parameter not recognized'}, 400   # return 400 otherwise
