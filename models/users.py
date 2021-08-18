# SQLAlchemy
from db import db
# function to encrypt given password
from utilities import bcrypt_hash


# The model for the user. The 'user' database holds 5 columns:
# id, username, password, created date, updated date.
# Id is the id of the user, which will be generated by server.
# Username and password are chosen by the user
# Upon registration, password is stored securely (hashed) in the database.
# Created is the date the user was created
# Updated date is the latest time when the user data was updated
class UserModel(db.Model):
    __tablename__ = 'user'      # initialize table
    # generated id of the user
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # the username chosen by the user
    username = db.Column(db.String(80), nullable=False, unique=True)
    # password of the user
    password = db.Column(db.String(2048), nullable=False)
    # created date of the category
    created = db.Column(db.DateTime(timezone=True),
                        server_default=db.func.now(),
                        nullable=False)
    # updated date of the category
    updated = db.Column(db.DateTime(timezone=True),
                        server_default=db.func.now(),
                        onupdate=db.func.now(),
                        nullable=False)
    # items that the user created
    items = db.relationship('ItemModel', lazy='dynamic')

    # initialization function
    def __init__(self, username, password):
        self.username = username                    # set username
        self.password = bcrypt_hash(password)       # hash and set password

    # find the user object by (unique) username
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # find the user object by (unique) id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # save object to database
    def save_to_db(self):
        db.session.add(self)                  # add the user to database
        db.session.commit()                   # commit changes

    # delete object from database
    def delete_from_db(self):
        db.session.delete(self)               # delete the user from database
        db.session.commit()                   # commit changes
