from flask import Flask, render_template
from flask_ask import Ask, statement, question
import json
import requests

app = Flask(__name__)
ask = Ask(app, "/")
consumer_key='17f7ebda44884922819ed3af418aa7d5'
consumer_secret='79a0301cfd6847b2bd40cca8a3c9fa16'

# def get_food_nutritions(food_name):
#     food_id = nix.search(food_name, results="0:1").json()['hits'][0]['_id']
#     food_result = nix.item(id=food_id).json()
#     return { 'protein': food_result['nf_protein'],
#              'carbs':   food_result['nf_total_carbohydrate'],
#              'fat':     food_result['nf_total_fat']}
#
# url = 'https://trackapi.nutritionix.com/v2/search/instant?query=potato'
# headers = { 'x-app-id': app_id, 'x-app-key': api_key }
# r = requests.get(url, headers=headers)
# headers = { 'Content-Type': 'application/json',
#             'x-app-id': '7ca440b2',
#             'x-app-key': 'e3a141ab25b4e8516ea8cde5bdc19474',
#             'x-remote-user-id': '123123123weas'}
#
# r = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', headers = headers, data = {'query':'tomato'})
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
    # result = get_food_nutritions(food_name)
    # food_info_msg = render_template(food_info, result)
    food_info_msg = "I find %s. Proteins %d, carbs %d, fat %d." % ('potato', 5, 60, 3)
    return statement(food_info_msg)

if __name__ == '__main__':
    app.run(debug=True)
