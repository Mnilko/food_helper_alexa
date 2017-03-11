from app import Blueprint, question, session, ask
from models import *

user_intent = Blueprint('user_intent', __name__)

@ask.intent("DefineUserIntent", mapping={'user_name': 'Name'})
def get_user(user_name):
    user = User.query.filter(User.name == user_name).first()
    if (user is None):
        session.attributes['user_name'] = user_name
        response_msg = "I can't find user. Should I create user with %s name?" % user_name
    else:
        session.attributes['user_id'] = user.id
        response_msg = "Hi %s, I'm glad to see you again!!! What you want to do next?" % user_name
    return question(response_msg)

@ask.intent("CreateUserIntent")
def create_user():
    if session.attributes['user_name']:
        new_user = User(name=session.attributes['user_name'])
        db.session.add(new_user)
        db.session.commit()
        session.attributes['user_id'] = new_user.id
        response_msg = 'User with name %s created.' % session.attributes['user_name']
    else:
        response_msg = "Can't create user with these name."
    return question(response_msg)
