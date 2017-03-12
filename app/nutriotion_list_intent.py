from app import Blueprint, question, ask, session
from models import *

nutriotion_list_intent = Blueprint('nutriotion_list_intent', __name__)

@ask.intent("MyNutritionIntent")
def get_nutriotion_list():
    if 'user_id' not in session.attributes:
        return question("Can't find without user. What is your name?")
    else:
        user = User.query.get(session.attributes['user_id'])
        user_info_list = "Your nutrion list is: proteins %i, carbs %i, fats %i." % (user.protein, user.carb, user.fat)
        return question(user_info_list)

@ask.intent("ChangeNutritionList", mapping={'nutrition': 'Nutrition', 'value': 'Value'})
def change_nutrition_value(nutrition, value):
    if ('user_id' not in session.attributes):
        return question("Can't find without user. What is your name?")
    elif (nutrition is None) | (value is None):
        return question("Please, provide nutriotion and amout.")
    else:
        user = User.query.get(session.attributes['user_id'])
        setattr(user, nutrition, int(value))
        db.session.commit()
        response_msg = "%s goal setted to %s" % (nutrition, user.__getattribute__(nutrition))
        return question(response_msg)
