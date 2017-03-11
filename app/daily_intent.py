from app import ask, Blueprint, session, question
from models import *

daily_intent = Blueprint('daily_intent', __name__)

@ask.intent('CurrentDailyIntent')
def current_intent(self, arg):
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
    elif ('nutrition' is None) | ('value' is None):

    else:
        user = User.query.get(session.attributes['user_id'])
        daily = Daily.query.filter(Daily.users.contains(user) & (Daily.created_timestamp >= datetime.date.today())).first()
        setattr(daily, , 10)
