from flask import render_template, redirect, url_for, flash
from learn_italian_flask import app
from learn_italian_flask import db
from learn_italian_flask.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user, login_required
from learn_italian_flask.models import User

from learn_italian_flask.forms import AlphabetQuizForm, NumbersQuizForm, GreetingsQuizForm, ColoursQuizForm, ArticlesQuizForm, VerbsQuizForm
from learn_italian_flask.models import AlphabetQuiz, NumbersQuiz, GreetingsQuiz, ColoursQuiz, ArticlesQuiz, VerbsQuiz
from learn_italian_flask.controllers import UserController, QuizController, LearnController, DashboardController, ResultsController

@app.route('/')
@app.route('/index')
def index():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))
    return render_template('index.html', title="Learn Italian")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return UserController.login()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return UserController.signup()

@app.route('/logout')
def logout():
    return UserController.logout()

@app.route('/dashboard')
@login_required    
def dashboard():
    return DashboardController.get_dashboard_homepage()

@app.route('/learn')
@login_required 
def learn():
    return LearnController.get_learn_homepage()

@app.route('/alphabet')
@login_required 
def alphabet():
    # return LearnController.get_alphabet_content()
    return LearnController.get_content("alphabet")

@app.route('/numbers')
@login_required 
def numbers():
    # return LearnController.get_numbers_content()
    return LearnController.get_content("numbers")

@app.route('/greetings')
@login_required 
def greetings():
    # return LearnController.get_greetings_content()
    return LearnController.get_content("greetings")

@app.route('/colours')
@login_required 
def colours():
    # return LearnController.get_colours_content()
    return LearnController.get_content("colours")

@app.route('/articles')
@login_required 
def articles():
    # return LearnController.get_articles_content()
    return LearnController.get_content("articles")

@app.route('/verbs')
@login_required 
def verbs():
    # return LearnController.get_verbs_content()
    return LearnController.get_content("verbs")

@app.route('/alphabet_quiz', methods=['GET', 'POST'])
@login_required 
def alphabet_quiz():
    return QuizController.get_alphabet_quiz()

@app.route('/numbers_quiz', methods=['GET', 'POST'])
@login_required 
def numbers_quiz():
    return QuizController.get_numbers_quiz()

@app.route('/greetings_quiz', methods=['GET', 'POST'])
@login_required 
def greetings_quiz():
    return QuizController.get_greetings_quiz()

@app.route('/colours_quiz', methods=['GET', 'POST'])
@login_required 
def colours_quiz():
    return QuizController.get_colours_quiz()

@app.route('/articles_quiz', methods=['GET', 'POST'])
@login_required 
def articles_quiz():
    return QuizController.get_articles_quiz()

@app.route('/verbs_quiz', methods=['GET', 'POST'])
@login_required 
def verbs_quiz():
    return QuizController.get_verbs_quiz()

@app.route('/results')
@login_required 
def results():
    return ResultsController.get_results()