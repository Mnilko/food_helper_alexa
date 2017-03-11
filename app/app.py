from flask import Flask
from flask_ask import Ask, statement, question
from fatsecret import Fatsecret
import json

app = Flask(__name__)
ask = Ask(app, "/")
consumer_key = '17f7ebda44884922819ed3af418aa7d5'
consumer_secret = '79a0301cfd6847b2bd40cca8a3c9fa16'
fs = Fatsecret(consumer_key, consumer_secret)

@ask.launch
def greeter():
    greeter_msg = 'Food helper serve you.'
    return question(greeter_msg)

@ask.intent("HelpIntent")
def helper():
    helper_msg = 'You can ask for nutritions.'
    return statement(helper_msg)

@ask.intent("FoodInfoIntent", mapping={'food_name': 'Food'})
def food_info(food_name):
    food_descript = fs.foods_search(food_name)[0]['food_description']
    food_info_msg = "I find %s. %s" % (food_name, food_descript)
    return statement(food_info_msg)

if __name__ == '__main__':
    app.run(debug=True)
