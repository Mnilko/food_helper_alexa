from app import Blueprint, question, ask, session
from models import *

nutriotion_list_intent = Blueprint('nutriotion_list_intent', __name__)

@ask.intent("MyNutrionIntent")
def get_nutriotion_list():
    if 'user_id' not in session.attributes:
        return question("Can't find without user. What is your name?")
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
