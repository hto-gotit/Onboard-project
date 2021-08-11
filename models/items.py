from db import db


class ItemModel(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    category = db.relationship('CategoryModel')
    user = db.relationship('UserModel')

    def __init__(self, name, description, category_id, user_id):
        self.name = name
        self.description = description
        self.category_id = category_id
        self.user_id = user_id

    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'category_id': self.category_id,
                'user_id': self.user_id, 'create': str(self.created), 'update': str(self.updated)}

    @classmethod
    def find_by_id(cls, item_id):
        return cls.query.filter_by(id=item_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
