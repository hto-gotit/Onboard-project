# SQLAlchemy exceptions
import sqlalchemy.exc
# Flask class & json functions
from flask import Flask, json
# restful API
from flask_restful import Api
# JWT manager
from flask_jwt_extended import JWTManager
# Http exceptions
from werkzeug.exceptions import HTTPException
# Handle command line arguments
import argparse

# resource to register
from resources.users import UserRegister
# resource to login
from resources.login import UserLogin
# all item-related resource
from resources.items import Item, CategoryItems, AllItems
# resource to get all categories
from resources.categories import CategoryList
# category models to create default category
from models.categories import CategoryModel

# Instantiate the Flask application
app = Flask(__name__)
# Commandline argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-env", "--environment",
                required=True,
                help="sepcify the environment of the app: "
                     "test, develop, or production")
args = vars(ap.parse_args())

# Use configuration according to environment
if args['environment'] == 'test':
    from config import config_test
    configFile = config_test
elif args['environment'] == 'develop':
    from config import config_develop
    configFile = config_develop
else:
    from config import config_production
    configFile = config_production

# database credential
app.config['SQLALCHEMY_DATABASE_URI'] \
    = 'mysql+pymysql://{}:{}@{}/{}'.format(configFile.mySQLusername,
                                           configFile.mySQLpassword,
                                           configFile.host,
                                           configFile.dbname)
# Track modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']\
    = configFile.trackModification
# Secret key for app
app.secret_key = configFile.secretKey
# Instantiate the API
api = Api(app)


# Handle HTTP Exceptions
@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        'status code': e.code,
        'name': e.name,
        'description': e.description,
    })
    response.content_type = "application/json"
    return response


# Handle all Exceptions
@app.errorhandler(Exception)
def internal_server_error_500(e):
    return {'message': 'Internal Server Error', 'error': e.args[0]}, 500


@app.before_first_request               # Create all tales in database
def create_tables():
    db.drop_all()                   # drop all past tables
    db.create_all()                 # create all tables
    # Create some default category
    try:
        cat1 = CategoryModel("First category")
        cat2 = CategoryModel("Second category")
        cat3 = CategoryModel("Third category")
        cat1.save_to_db()
        cat2.save_to_db()
        cat3.save_to_db()
    except sqlalchemy.exc.IntegrityError:
        pass


# Instantiate the JWT manager
jwt = JWTManager(app)

# Declare all the Resources for the API
api.add_resource(CategoryList, '/categories')
# api.add_resource(Category, '/categories/<int:category_id>')
api.add_resource(CategoryItems, '/categories/<int:category_id>/items')
api.add_resource(Item, '/categories/<int:category_id>/items/<int:item_id>')
api.add_resource(AllItems, '/items')
api.add_resource(UserRegister, '/users')
# api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/auth/login')

# if running in main
if __name__ == '__main__':
    # SQLAlchemy
    from db import db
    # Instantiate the database
    db.init_app(app)
    # Run application
    app.run(port=configFile.port, debug=configFile.debug)
