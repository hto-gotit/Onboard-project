from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.users import UserRegister, User
from resources.login import UserLogin
from resources.items import Item, ItemList, ItemCreate
from resources.categories import Category, CategoryList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password1!@localhost/catalogdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'SecRetPassWord123*()'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api.add_resource(ItemList, '/categories/<int:category_id>/items')
api.add_resource(Item, '/categories/<int:category_id>/items/<int:item_id>')
api.add_resource(ItemCreate, '/categories/<int:category_id>/items')
api.add_resource(CategoryList, '/categories')
api.add_resource(Category, '/categories/<int:category_id>')
api.add_resource(UserRegister, '/users')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
