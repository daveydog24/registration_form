from flask import Flask, render_template, request, redirect, flash, session
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'RegistrationAssignment'
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$')
name_regex = re.compile(r'/^([^0-9]*)$/')

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if 'count_test' not in session:
        session['count_test'] = 0

    if email_regex.match(email):
        session['email'] = email
        session['count_test'] += 1
    else:
        flash('invalid email address, try again')
    if len(first_name) > 0 and name_regex.match(first_name):
        session['first_name'] = first_name
        session['count_test'] += 1
    else:
        flash('invalid first name input, try again')
    if len(last_name) > 0 and name_regex.match(last_name):
        session['last_name'] = last_name
        session['count_test'] += 1
    else:
        flash('invalid last name input, try again')
    if password_regex.match(password):
        if password_regex.match(confirm_password):
            if confirm_password == password:
                session['password'] = password
                session['confirm_password'] = confirm_password
                session['count_test'] += 1
            else:
                flash('password does not match, try again')  
    else:
        flash('invalid password format, try again')

    if int(session['count_test']) == 4:
        flash("Thanks for submitting your information.")
        return render_template("results.html", email=session['email'], first_name=session['first_name'], last_name=session['last_name'], password=session['password'], confirm_password=session['confirm_password'])
    else:
        session.pop('count_test')
        return redirect('/')

app.run(debug=True)