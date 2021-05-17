from flask import render_template, redirect, url_for, flash
from learn_italian_flask import app
from learn_italian_flask import db
from learn_italian_flask.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user, login_required
from learn_italian_flask.models import User, Quiz, UserAnswer

from learn_italian_flask.forms import QuizForm
from learn_italian_flask.controllers import get_index, get_statistics, user_login, user_signup, user_logout, get_dashboard_homepage, get_learning_homepage, get_learning_content, get_quiz, get_results

@app.route('/')
@app.route('/index')
def index():
    return get_index()

@app.route('/statistics')
def statistics():
    return get_statistics()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return user_login()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return user_signup()

@app.route('/logout')
def logout():
    return user_logout()

@app.route('/dashboard')
@login_required    
def dashboard():
    return get_dashboard_homepage()

@app.route('/learn')
@login_required 
def learn():
    return get_learning_homepage()

@app.route('/alphabet')
@login_required 
def alphabet():
    return get_learning_content("alphabet")

@app.route('/numbers')
@login_required 
def numbers():
    return get_learning_content("numbers")

@app.route('/greetings')
@login_required 
def greetings():
    return get_learning_content("greetings")

@app.route('/colours')
@login_required 
def colours():
    return get_learning_content("colours")

@app.route('/articles')
@login_required 
def articles():
    return get_learning_content("articles")

@app.route('/verbs')
@login_required 
def verbs():
    return get_learning_content("verbs")

@app.route('/alphabet_quiz', methods=['GET', 'POST'])
@login_required 
def alphabet_quiz():
    return get_quiz("Alphabet")

@app.route('/numbers_quiz', methods=['GET', 'POST'])
@login_required 
def numbers_quiz():
    return get_quiz("Numbers")

@app.route('/greetings_quiz', methods=['GET', 'POST'])
@login_required 
def greetings_quiz():
    return get_quiz("Greetings")

@app.route('/articles_quiz', methods=['GET', 'POST'])
@login_required 
def articles_quiz():
    return get_quiz("Articles")


@app.route('/colours_quiz', methods=['GET', 'POST'])
@login_required 
def colours_quiz():
    return get_quiz("Colours")

@app.route('/verbs_quiz', methods=['GET', 'POST'])
@login_required 
def verbs_quiz():
    return get_quiz("Verbs")

@app.route('/results')
@login_required 
def results():
    return get_results()
