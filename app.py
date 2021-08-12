from flask import Flask                                     # import Flask class
from flask_restful import Api                               # import restful API
from flask_jwt_extended import JWTManager                   # import JWT manager

from resources.users import UserRegister                    # import resource to register
# from resources.users import User                          # import User resource (not available to users)
from resources.login import UserLogin                       # import resource to login
from resources.items import Item, ItemList, ItemLatests     # import all item-related resource
from resources.categories import CategoryList               # import resource to get all categories
# from resources.categories import Category                 # import Category resource (not available to users)

app = Flask(__name__)                                       # Instantiate the Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password1!@localhost/catalogdb'  # path to database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # Disable tracking modifications
app.config['PROPAGATE_EXCEPTIONS'] = True                   # Enable tracking exceptions
app.secret_key = 'SecRetPassWord123*()'                     # Secret key for app
api = Api(app)                                              # Instantiate the API


@app.before_first_request               # Create all tales in database
def create_tables():
    db.create_all()


jwt = JWTManager(app)                   # Instantiate the JWT manager

# Declare all the Resources for the API
api.add_resource(CategoryList, '/categories')
# api.add_resource(Category, '/categories/<int:category_id>')
api.add_resource(ItemList, '/categories/<int:category_id>/items')
api.add_resource(Item, '/categories/<int:category_id>/items/<int:item_id>')
api.add_resource(ItemLatests, '/items')
api.add_resource(UserRegister, '/users')
# api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/auth/login')

# if running in main
if __name__ == '__main__':
    from db import db                       # import SQLAlchemy
    db.init_app(app)                        # Instantiate the database
    app.run(port=5000, debug=True)          # Run application
