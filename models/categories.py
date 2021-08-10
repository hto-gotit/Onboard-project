from db import db
import datetime


class CategoryModel(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    items = db.relationship('ItemModel', backref='category', lazy=True)

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.commit()

