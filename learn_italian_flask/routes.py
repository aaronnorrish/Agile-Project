from flask import render_template, redirect, url_for, flash
from learn_italian_flask import app
from learn_italian_flask import db
from learn_italian_flask.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user, login_required
from learn_italian_flask.models import User

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
    return render_template('dashboard.html', title="Dashboard")

@app.route('/learn')
@login_required 
def learn():
    return render_template('learn.html', title="Learn")

@app.route('/alphabet')
@login_required 
def alphabet():
    return render_template('alphabet.html', title="Alphabet")
