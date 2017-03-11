from flask import Flask
from flask_ask import Ask, statement, question, session
from fatsecret import Fatsecret
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from config import Configuration

app = Flask(__name__)
ask = Ask(app, "/")
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import *

manager = Manager(app)
manager.add_command('db', MigrateCommand)

consumer_key = '17f7ebda44884922819ed3af418aa7d5'
consumer_secret = '79a0301cfd6847b2bd40cca8a3c9fa16'
fs = Fatsecret(consumer_key, consumer_secret)

@ask.launch
def greeter():
    ask_msg = 'Hi, there! What is your name?'
    return question(ask_msg)

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

@ask.intent("AMAZON.NoIntent")
def no_handler():
    if session.attributes['user_name']:
        response_msg = 'You can only ask about food info without user.'
    return statement(response_msg)

@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def trip_nogo():
    quit_msg = "Good luck in gym."
    return statement(quit_msg)

@ask.intent("HelpIntent")
def helper():
    helper_msg = 'You can ask for nutritions.'
    return question(helper_msg)

@ask.intent("FoodInfoIntent", mapping={'food_name': 'Food'})
def food_info(food_name):
    try:
        food_result = fs.foods_search(food_name)
        food_descript = food_result[0]['food_description']
        food_info_msg = "I find %s. %s" % (food_name, food_descript)
        return question(food_info_msg)
    except KeyError:
        food_info_msg = "I can't find these food."
        return question(food_info_msg)

@ask.intent("MyNutrionIntent")
def get_nutriotion_list():
    if 'user_id' not in session.attributes:
        return question("Can't change without user. What is your name?")
    else:
        user = User.query.get(session.attributes['user_id'])
        user_info_list = "Your nutrion list is: proteins %i, carbs %i, fats %i." % (user.protein, user.carb, user.fat)
        return question(user_info_list)

@ask.intent("ChangeProteinIntent", mapping={'value': 'Value'})
def change_protein_value(value):
    if 'user_id' not in session.attributes:
        return question("Can't change without user. What is your name?")
    else:
        user = User.query.get(session.attributes['user_id'])
        user.protein = int(value)
        db.session.commit()
        result_msg = "Your protein goal set to %s grams per day." % value
        return question(result_msg)

@ask.intent("ChangeCarbIntent", mapping={'value': 'Value'})
def change_carb_value(value):
    if 'user_id' not in session.attributes:
        return question("Can't change without user. What is your name?")
    else:
        user = User.query.get(session.attributes['user_id'])
        user.carb = int(value)
        db.session.commit()
        result_msg = "Your carb goal set to %s grams per day." % value
        return question(result_msg)

@ask.intent("ChangeFatIntent", mapping={'value': 'Value'})
def change_fat_value(value):
    if 'user_id' not in session.attributes:
        return question("Can't change without user. What is your name?")
    else:
        user = User.query.get(session.attributes['user_id'])
        user.fat = int(value)
        db.session.commit()
        result_msg = "Your fat goal set to %s grams per day." % value
        return question(result_msg)

if __name__ == '__main__':
    app.run(debug=True)
