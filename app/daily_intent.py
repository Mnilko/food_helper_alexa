from app import ask, Blueprint, session, question
from models import *

daily_intent = Blueprint('daily_intent', __name__)

@ask.intent('CurrentDailyIntent')
def current_intent():
    if 'user_id' not in session.attributes:
        return question("Can't find without user. What is your name?")\
          .repromt("Please provide name or use food search.")
    else:
        user = User.query.get(session.attributes['user_id'])
        daily = Daily.query.filter(Daily.users.contains(user) & (Daily.created_timestamp >= datetime.date.today())).first()
        if daily is None:
            daily = Daily()
            user.dailies.append(daily)
            db.session.add(daily)
            db.session.commit()
            response_msg = "You didn't add any food today. Do you want to add something?"
        else:
            response_msg = "You ate %i proteins, %i carbs, %i fats today." % (daily.protein, daily.carb, daily.fat)
        return question(response_msg)\
          .reprompt("Do you want to continue?")

@ask.intent('DailyAddNutritionIntent', mapping={'nutrition': 'Nutrition', 'value': 'Value'})
def add_nutriotion(nutrition, value):
    if ('user_id' not in session.attributes):
        return question("Can't find without user. What is your name?")\
          .repromt("Please provide name or use food search.")
    elif (nutrition is None) | (value is None):
        response_msg = "Please, provide nutrition and amout."
    else:
        user = User.query.get(session.attributes['user_id'])
        daily = Daily.query.filter(Daily.users.contains(user) & (Daily.created_timestamp >= datetime.date.today())).first()
        if daily is None:
            daily = Daily()
            user.dailies.append(daily)
            db.session.add(daily)
            db.session.commit()
        sum_value = daily.__getattribute__(nutrition) + int(value)
        setattr(daily, nutrition, sum_value)
        db.session.commit()
        response_msg = "You ate %i %s" % (sum_value, nutriotion)
    return question(response_msg)\
      .reprompt("Do you want to continue?")

@ask.intent('DailyAddNutritionListIntent', mapping={'protein': 'Protein', 'fat': 'Fat', 'carb': 'Carb'})
def add_nutriotion_list(protein, fat, carb):
    if ('user_id' not in session.attributes):
        return question("Can't find without user. What is your name?")\
          .repromt("Please provide name or use food search.")
    elif (protein is None) | (fat is None) | (carb is None):
        response_msg = "Please, provide nutriotion and amout."
    else:
        user = User.query.get(session.attributes['user_id'])
        daily = Daily.query.filter(Daily.users.contains(user) & (Daily.created_timestamp >= datetime.date.today())).first()
        if daily is None:
            daily = Daily()
            user.dailies.append(daily)
            db.session.add(daily)
            db.session.commit()
        setattr(daily, 'protein', (daily.protein + int(protein)))
        setattr(daily, 'fat', (daily.fat + int(fat)))
        setattr(daily, 'carb', (daily.carb + int(carb)))
        db.session.commit()
        response_msg = "Your updated daily summary: %s proteins, %s carbs, %s fats" % (daily.protein, daily.carb, daily.fat)
    return question(response_msg)\
      .reprompt("Do you want to continue?")

@ask.intent('DailyLeftNutritionIntent')
def left_nutriotion():
    if ('user_id' not in session.attributes):
        return question("Can't find without user. What is your name?")\
          .repromt("Please provide name or use food search.")
    else:
        user = User.query.get(session.attributes['user_id'])
        daily = Daily.query.filter(Daily.users.contains(user) & (Daily.created_timestamp >= datetime.date.today())).first()
        if daily is None:
            daily = Daily()
            user.dailies.append(daily)
            db.session.add(daily)
            db.session.commit()
            response_msg = "You didn't add any food today. Do you want to add something?"
        else:
            protein_left = user.protein - daily.protein
            carb_left = user.carb - daily.carb
            fat_left = user.fat - daily.fat
            response_msg = "You need to eat: %i protein, %i carbs, %i fat." % (protein_left, carb_left, fat_left)
        return question(response_msg)\
          .reprompt("Do you want to continue?")
