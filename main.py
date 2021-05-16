from learn_italian_flask import app, db
from learn_italian_flask.models import User, Quiz, UserAnswer

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, "Quiz": Quiz, "UserAnswer": UserAnswer}