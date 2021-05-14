from learn_italian_flask import app, db
from learn_italian_flask.models import User, AlphabetQuiz, NumbersQuiz, GreetingsQuiz, ColoursQuiz, ArticlesQuiz, VerbsQuiz, Quiz, UserAnswer

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'AlphabetQuiz': AlphabetQuiz, 'NumbersQuiz': NumbersQuiz, 'GreetingsQuiz': GreetingsQuiz, 'ColoursQuiz': ColoursQuiz, 'ArticlesQuiz': ArticlesQuiz, 'VerbsQuiz': VerbsQuiz, "Quiz": Quiz}