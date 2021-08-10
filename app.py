from flask import Flask
from flask.json import jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Api
import mysql.connector
from flask_jwt_extended import JWTManager

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'Project_onboard!@#'
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000)