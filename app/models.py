import datetime, re

from app import db

class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    protein = db.Column(db.Integer)
    carb = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, *args, **kwards) :
        super(User, self).__init__(*args, **kwards)

    def __repr__(self):
        return '<User: %s>' % self.name
