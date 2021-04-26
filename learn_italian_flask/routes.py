from flask import render_template, redirect, url_for
from learn_italian_flask import app
from learn_italian_flask.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Learn Italian")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # TODO haven't added a flash error as in the tutorial
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    return render_template('log-in.html', title="Learn Italian - Log in", form=form)

@app.route('/signup')
def signup():
    return render_template('sign-up.html', title="Learn Italian - Sign up")

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title="Dashboard", user={'name': '[placeholder]'})

@app.route('/learn')
def learn():
    return render_template('learn.html', title="Learn")
