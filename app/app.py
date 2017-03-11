from flask import Flask, Blueprint
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

@ask.launch
def greeter():
    ask_msg = 'Hi, there! What is your name?'
    return question(ask_msg)

@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent("AMAZON.NoIntent")
def bye_bye():
    quit_msg = "Good luck in gym."
    return statement(quit_msg)

@ask.intent("HelpIntent")
def helper():
    helper_msg = 'You can ask for nutritions.'
    return question(helper_msg)

if __name__ == '__main__':
    app.run(debug=True)
