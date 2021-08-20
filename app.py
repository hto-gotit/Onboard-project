# Flask class & json functions
from flask import Flask
# restful API
from flask_restful import Api
# JWT manager
from flask_jwt_extended import JWTManager, exceptions
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
# Instantiate the JWT manager
jwt = JWTManager(app)

# Register custom errors handler
app.register_error_handler(ParentException, handle_custom_errors)

# Register jwt, HTTP errors handler and default error handler
app.register_error_handler(HTTPException, handle_http_exception)
app.register_error_handler(exceptions.NoAuthorizationError, handle_missing_jwt)
app.register_error_handler(Exception, default_handler)

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
