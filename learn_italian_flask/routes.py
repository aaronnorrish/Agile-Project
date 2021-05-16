from flask import render_template, redirect, url_for, flash
from learn_italian_flask import app
from learn_italian_flask import db
from learn_italian_flask.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user, login_required
from learn_italian_flask.models import User

from learn_italian_flask.forms import QuizForm
from learn_italian_flask.models import Quiz, UserAnswer
from learn_italian_flask.controllers import UserController, QuizController, LearnController, DashboardController, ResultsController

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Learn Italian")

@app.route('/statistics')
def statistics():
    # TODO move to controller!!
    all_user_quizzes = UserAnswer.query.all()
    num_quizzes_completed = sum([1 for quiz in all_user_quizzes])
    print(num_quizzes_completed)
    all_quizzes = Quiz.query.all()

    labels = []
    if all_quizzes is not None:
        labels = [quiz.name for quiz in all_quizzes]
    cumulative_scores = [0 for i in range(len(labels))]
    attempts = [0 for i in range(len(labels))]
    for quiz in all_user_quizzes:
        cumulative_scores[quiz.quiz_id-1] += quiz.score * 100
        attempts[quiz.quiz_id-1] += 1
    scores = [round(score/attempt) if attempt != 0 else 0 for score, attempt in zip(cumulative_scores, attempts)]

    users = User.query.all()
    num_users = sum([1 for user in users])
    print(num_users)
    return render_template('statistics.html', title="Learn Italian — Usage Statistics", labels=labels, scores=scores, num_users=num_users, num_quizzes_completed=num_quizzes_completed)

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
    return LearnController.get_content("alphabet")

@app.route('/numbers')
@login_required 
def numbers():
    return LearnController.get_content("numbers")

@app.route('/greetings')
@login_required 
def greetings():
    return LearnController.get_content("greetings")

@app.route('/colours')
@login_required 
def colours():
    return LearnController.get_content("colours")

@app.route('/articles')
@login_required 
def articles():
    return LearnController.get_content("articles")

@app.route('/verbs')
@login_required 
def verbs():
    return LearnController.get_content("verbs")

@app.route('/alphabet_quiz', methods=['GET', 'POST'])
@login_required 
def alphabet_quiz():
    return QuizController.get_quiz("Alphabet")

@app.route('/numbers_quiz', methods=['GET', 'POST'])
@login_required 
def numbers_quiz():
    return QuizController.get_quiz("Numbers")

@app.route('/greetings_quiz', methods=['GET', 'POST'])
@login_required 
def greetings_quiz():
    return QuizController.get_quiz("Greetings")

@app.route('/articles_quiz', methods=['GET', 'POST'])
@login_required 
def articles_quiz():
    return QuizController.get_quiz("Articles")


@app.route('/colours_quiz', methods=['GET', 'POST'])
@login_required 
def colours_quiz():
    return QuizController.get_quiz("Colours")

@app.route('/verbs_quiz', methods=['GET', 'POST'])
@login_required 
def verbs_quiz():
    return QuizController.get_quiz("Verbs")

@app.route('/results')
@login_required 
def results():
    return ResultsController.get_results()
