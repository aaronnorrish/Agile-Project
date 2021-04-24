from flask import render_template
from learn_italian_flask import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Learn Italian")

@app.route('/login')
def login():
    return render_template('log-in.html', title="Learn Italian - Log in")

@app.route('/signup')
def signup():
    return render_template('sign-up.html', title="Learn Italian - Sign up")

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title="Dashboard", user={'name': '[placeholder]'})

@app.route('/learn')
def learn():
    return render_template('learn.html', title="Learn")
