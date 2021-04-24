from flask import render_template
from learn_italian_flask import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Learn Italian")
    # return render_template('dashboard.html', title="Dashboard", user={'name': '[placeholder]'})

@app.route('/login')
def login():
    return render_template('log-in.html', title="Learn Italian - Log in")

@app.route('/signup')
def signup():
    return render_template('sign-up.html', title="Learn Italian - Sign up")
