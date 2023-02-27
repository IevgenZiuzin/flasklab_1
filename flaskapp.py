import os
import random
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())


@app.route("/")
def index():
    message = 'Hello, world!'
    context = {
        'message': message
    }
    return render_template('index.html', context=context)


@app.route("/weekday")
def weekday():
    time_now = datetime.now()
    day = time_now.strftime('%A')
    context = {
        'day': day
    }
    return render_template('weekday.html', context=context)


@app.route("/quote")
def quote():
    rand_id = random.randrange(0, db.session.query(Quote).count())
    user_quote = db.session.query(Quote)[rand_id]
    context = {
        'quote': user_quote
    }
    return render_template('quote.html', context=context)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
