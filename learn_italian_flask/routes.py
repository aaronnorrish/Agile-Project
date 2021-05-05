from flask import render_template, redirect, url_for, flash
from learn_italian_flask import app
from learn_italian_flask import db
from learn_italian_flask.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user, login_required
from learn_italian_flask.models import User

from learn_italian_flask.forms import AlphabetQuizForm
from learn_italian_flask.models import TestQuiz

@app.route('/')
@app.route('/index')
def index():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))
    return render_template('index.html', title="Learn Italian")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    # TODO haven't added a flash error as in the tutorial
    # if want to render the flash messages need to add this to the HTML template
    # as in the chapter 3 of the tutorial
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('log-in.html', title="Learn Italian - Log in", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        # flash('Sign up was successful!')
        return redirect(url_for('dashboard'))
    return render_template('sign-up.html', title="Learn Italian - Sign up", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required    
def dashboard():
    modules = []
    if current_user.get_next_module() == "alphabet":
        modules.append("cards/_alphabet_card.html")
    return render_template('dashboard.html', title="Dashboard", progress=current_user.get_progress(), modules=modules)

@app.route('/learn')
@login_required 
def learn():
    return render_template('learn.html', title="Learn")

@app.route('/alphabet')
@login_required 
def alphabet():
    return render_template('alphabet.html', title="Learn - Alphabet")

# TODO think we can make a general function to handle any quiz
# maybe need to make a quiz template?
# maybe saving qx_correct is redundant because when we look at the responses we want to see what the
# correct answer is so will have to load the actual solution each time anyway
# TODO current problem: question 1 is not being disabled and the other fields are disabled
#   even if no attempt has been made yet
#   solution could be to disable it in the html; even if this is removed by client it wont actually cause any changes in the database
@app.route('/alphabet_quiz', methods=['GET', 'POST'])
@login_required 
def alphabet_quiz():
    form = AlphabetQuizForm()
    completed = False
    prev_attempt = TestQuiz.query.filter_by(testee_id=current_user.id).first()
    solution = None
    if prev_attempt is not None:
        completed = True
        form.question1.data = prev_attempt.q1
        # form.question1.render_kw['disabled'] = 'true'
        form.question2.data = prev_attempt.q2
        # form.question2.render_kw['disabled'] = 'true'
        # form.submit.render_kw['disabled'] = 'true'
        solution = TestQuiz.query.filter_by(id=99).first()
        solution = {"q1": solution.q1, "q1_correct": solution.q1 == prev_attempt.q1, "q2": solution.q2, "q2_correct": solution.q2 == prev_attempt.q2}
    elif form.validate_on_submit():
        answer1 = form.question1.data
        answer2 = form.question2.data
        print(answer1, answer2)
        curr_id = current_user.id
        sol = TestQuiz.query.filter_by(id=99).first()
        ans1_correct = answer1 == sol.q1
        ans2_correct = answer2 == sol.q2
        score = sum([1 if ans == True else 0 for ans in [ans1_correct, ans2_correct]]) / 2
        attempt = TestQuiz(testee_id=curr_id, q1=answer1, q1_correct=ans1_correct, q2=answer2, q2_correct=ans2_correct, score=score)
        db.session.add(attempt)
        db.session.commit()
    return render_template("quiz/test_quiz.html", title="Quiz - Alphabet", form=form, completed=completed, solution=solution)