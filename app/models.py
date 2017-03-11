import datetime, re

from app import db

user_daylies = db.Table('user_daylies',
    db.Column('daily_id', db.Integer, db.ForeignKey('daily.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    protein = db.Column(db.Integer, default=0)
    carb = db.Column(db.Integer, default=0)
    fat = db.Column(db.Integer, default=0)
    created_timestamp = db.Column(db.Date, default=datetime.date.today())

    dailies = db.relationship('Daily', secondary=user_daylies,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, *args, **kwards) :
        super(User, self).__init__(*args, **kwards)

    def __repr__(self):
        return '<User: %s>' % self.name

class Daily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protein = db.Column(db.Integer, default=0)
    carb = db.Column(db.Integer, default=0)
    fat = db.Column(db.Integer, default=0)
    created_timestamp = db.Column(db.Date, default=datetime.date.today())

    def __init__(self, *args, **kwards) :
        super(Daily, self).__init__(*args, **kwards)

    def __repr__(self):
        return '<Daily: protein %i, carb %i, fat %i.>' % (self.protein, self.carb, self.fat)
