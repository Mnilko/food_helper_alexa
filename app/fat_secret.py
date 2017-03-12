from app import ask, fs, question, Blueprint

fat_secret = Blueprint('fat_secret', __name__)

@ask.intent("FoodInfoIntent", mapping={'food_name': 'Food'})
def food_info(food_name):
    try:
        food_result = fs.foods_search(food_name)
        food_descript = food_result[0]['food_description']
        response_msg = "I find %s. %s" % (food_name, food_descript)
    except KeyError:
        response_msg = "I can't find these food."
    return question(response_msg)
