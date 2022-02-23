from flask import Flask, render_template, redirect, jsonify, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_gravatar import Gravatar
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "jyhtfrdyjtdyjtdyjdtyj"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False,
                    base_url=None)
db = SQLAlchemy(app=app)

bootstrap = Bootstrap(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(200), nullable=False)
    coffee_price = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

class NewCafeForm(FlaskForm):
    name = StringField(label="Cafe Name", validators=[DataRequired()])
    map_url = URLField(label="Map URL", validators=[DataRequired(), URL()])
    img_url = URLField(label="Image URL", validators=[DataRequired(), URL()])
    location = StringField(label='Location', validators=[DataRequired()])
    has_sockets = BooleanField(label="Has sockets?", validators=[DataRequired()])
    has_toilet = BooleanField(label="Has toilet?", validators=[DataRequired()])
    has_wifi = BooleanField(label="Has wifi?", validators=[DataRequired()])
    can_take_calls = BooleanField(label="Can take calls?", validators=[DataRequired()])
    seats = StringField(label="Number of seats", validators=[DataRequired()])
    coffee_price = StringField(label="Coffee price", validators=[DataRequired()])
    submit = SubmitField(label="Save", validators=[DataRequired()])


@app.route('/')
def home():
    cafes = Cafe.query.all()
    cafe_list = [cafe.to_dict() for cafe in cafes]
    return render_template("index.html", cafes=cafe_list)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form.get('search')
        cafes = [Cafe.query.filter_by(name=name).first()]
        return render_template('index.html', cafes=cafes, search=True)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = NewCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect('/')
    return render_template('new_cafe.html', form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
