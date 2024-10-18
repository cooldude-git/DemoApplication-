from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class CarForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired(), Length(min=1, max=50)])
    model = StringField('Model', validators=[DataRequired(), Length(min=1, max=50)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1886, max=2100)])

def get_db_connection():
    conn = sqlite3.connect('cars.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cars = conn.execute('SELECT * FROM cars').fetchall()
    conn.close()
    return render_template('index.html', cars=cars)

@app.route('/add', methods=('GET', 'POST'))
def add():
    form = CarForm()
    if form.validate_on_submit():
        make = form.make.data
        model = form.model.data
        year = form.year.data

        conn = get_db_connection()
        conn.execute('INSERT INTO cars (make, model, year) VALUES (?, ?, ?)',
                     (make, model, year))
        conn.commit()
        conn.close()
        flash('Car added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)