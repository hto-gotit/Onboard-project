# Flask class & json functions
from flask import Flask, json
# restful API
from flask_restful import Api
# JWT manager
from flask_jwt_extended import JWTManager
# Http exceptions
from werkzeug.exceptions import HTTPException

# resource to register
from resources.users import UserRegister
# resource to login
from resources.login import UserLogin
# all item-related resource
from resources.items import Item, CategoryItems, AllItems
# resource to get all categories
from resources.categories import CategoryList
# custom errors
from errors import *

# Instantiate the Flask application
app = Flask(__name__)

# Get app configuration
app.config.from_envvar('ENV')

# Instantiate the API
api = Api(app)

# Register custom errors handler
app.register_error_handler(CategoryDNE, handle_custom_errors)
app.register_error_handler(ItemDNE, handle_custom_errors)
app.register_error_handler(UserForbidden, handle_custom_errors)
app.register_error_handler(ItemNameDuplicate, handle_custom_errors)
app.register_error_handler(InvalidCredentials, handle_custom_errors)
app.register_error_handler(UsernameAlreadyExists, handle_custom_errors)

# Register HTTP errors handler and default error handler
app.register_error_handler(HTTPException, handle_http_exception)
app.register_error_handler(Exception, default_handler)


# Instantiate the JWT manager
jwt = JWTManager(app)


# JWT loaders for unauthorized
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {'message': 'Your token has expired'}, 401


@jwt.unauthorized_loader
def unauthorized_token_callback(jwt_header):
    return {'message': 'You are not logged in'}, 401


# Declare all the Resources for the API
api.add_resource(CategoryList, '/categories')
api.add_resource(CategoryItems, '/categories/<int:category_id>/items')
api.add_resource(Item, '/categories/<int:category_id>/items/<int:item_id>')
api.add_resource(AllItems, '/items')
api.add_resource(UserRegister, '/users')
api.add_resource(UserLogin, '/auth/login')

# if running in main
if __name__ == '__main__':
    # SQLAlchemy
    from db import db
    # Instantiate the database
    db.init_app(app)
    # Run application
    app.run()
