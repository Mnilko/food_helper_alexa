from flask import Flask, Blueprint, request
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
manager = Manager(app)
manager.add_command('db', MigrateCommand)

consumer_key = '17f7ebda44884922819ed3af418aa7d5'
consumer_secret = '79a0301cfd6847b2bd40cca8a3c9fa16'
fs = Fatsecret(consumer_key, consumer_secret)

from models import *
from fat_secret import fat_secret
from user_intent import user_intent
from nutriotion_list_intent import nutriotion_list_intent
from daily_intent import daily_intent

without_user = [
  'FoodInfoIntent','AMAZON.StopIntent', 'AMAZON.CancelIntent', "AMAZON.HelpIntent",
  'AMAZON.NoIntent', 'DefineUserIntent', 'CreateUserIntent', 'ChangeUserIntent'
]

@app.before_request
def before_request():
    intent = request.json['request']['intent']['name']
    if intent not in without_user:
      print('Intent name is %s' % intent)


@ask.launch
def greeter():
    ask_msg = 'Hi, there! What is your name?'
    return question(ask_msg)\
      .reprompt('Hi, there! What is your name?')


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def bye_bye():
    quit_msg = 'Good luck in gym.'
    return statement(quit_msg)

@ask.intent('AMAZON.HelpIntent')
def helper():
    helper_msg = 'You can search food info, set your daily nutriotion needs, calculate nutritions for current date.'
    return question(helper_msg)\
      .reprompt('You can search food info, set your daily nutriotion needs, calculate nutritions for current date.')

@ask.intent('AMAZON.NoIntent')
def no_handler():
    response_msg = 'You can search for food.'
    return question(response_msg)\
      .reprompt('You can search for food.')

if __name__ == '__main__':
    app.run(debug=True)
