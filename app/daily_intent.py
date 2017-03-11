from app import ask, Blueprint, session, question
from models import *

daily_intent = Blueprint('daily_intent', __name__)

@ask.intent('CurrentDailyIntent')
def current_intent():
    if 'user_id' not in session.attributes:
        return question("Can't find without user. What is your name?")
    else:
        user = User.query.get(session.attributes['user_id'])
        daily = Daily.query.filter(Daily.users.contains(user) & (Daily.created_timestamp >= datetime.date.today())).first()
        if daily is None:
            daily = Daily()
            user.dailies.append(daily)
            db.session.add(daily)
            db.session.commit()
            response_msg = "You didn't add any food today. Do you want to add something?"
            return question(response_msg)
        else:
            print(daily)
            response_msg = "You ate %i proteins, %i carbs, %i fats today." % (daily.protein, daily.carb, daily.fat)
            return question(response_msg)

@ask.intent('DailyAddNutritionIntent', mapping={'nutrition': 'Nutrition', 'value': 'Value'})
def add_nutriotion(nutrition, value):
    if ('user_id' not in session.attributes):
        return question("Can't find without user. What is your name?")
    elif (nutrition is None) | (value is None):
        return question("Please, provide nutriotion and amout.")
    else:
        user = User.query.get(session.attributes['user_id'])
        daily = Daily.query.filter(Daily.users.contains(user) & (Daily.created_timestamp >= datetime.date.today())).first()
        sum_value = daily.__getattribute__(nutrition) + int(value)
        setattr(daily, nutrition, sum_value)
        db.session.commit()
        response_msg = "You daily summary: %i proteins, %i carbs, %i fats." % (daily.protein, daily.carb, daily.fat)
        return question(response_msg)

@ask.intent('DailyLeftNutritionIntent')
def left_nutriotion():
    if ('user_id' not in session.attributes):
        return question("Can't find without user. What is your name?")
    else:
        user = User.query.get(session.attributes['user_id'])
        daily = Daily.query.filter(Daily.users.contains(user) & (Daily.created_timestamp >= datetime.date.today())).first()
        if daily is None:
            daily = Daily()
            user.dailies.append(daily)
            db.session.add(daily)
            db.session.commit()
            response_msg = "You didn't add any food today. Do you want to add something?"
            return question(response_msg)
        else:
            protein_left = user.protein - daily.protein
            carb_left = user.carb - daily.carb
            fat_left = user.fat - daily.fat
            response_msg = "You need to eat: %i protein, %i carbs, %i fat." % (protein_left, carb_left, fat_left)
            return question(response_msg)
