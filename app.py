import sqlalchemy.exc
from flask import Flask                               # import Flask class
from flask_restful import Api                         # import restful API
from flask_jwt_extended import JWTManager             # import JWT manager

# import resource to register
from resources.users import UserRegister
# import User resource (not available to users)
# from resources.users import User
# import resource to login
from resources.login import UserLogin
# import all item-related resource
from resources.items import Item, ItemList, ItemLatests
# import resource to get all categories
from resources.categories import CategoryList
# import Category resource (not available to users)
# from resources.categories import Category
from models.categories import CategoryModel

# Instantiate the Flask application
app = Flask(__name__)
# path to database
app.config['SQLALCHEMY_DATABASE_URI'] \
    = 'mysql+pymysql://root:Password1!@localhost/catalogdb'
# Disable tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Enable tracking exceptions
app.config['PROPAGATE_EXCEPTIONS'] = True
# Secret key for app
app.secret_key = 'SecRetPassWord123*()'
# Instantiate the API
api = Api(app)


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
