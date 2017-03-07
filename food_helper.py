from flask import Flask, render_template
from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def greeter():
    greeter_msg = render_template('greeting')
    return question(greeter_msg)

@ask.intent("HelpIntent")
def helper():
    helper_msg = render_template('helper')
    return statement(helper_msg)

if __name__ == '__main__':
    app.run(debug=True)
