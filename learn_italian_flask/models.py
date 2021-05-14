from learn_italian_flask import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# i think it makes sense to have each test represented as its own model
# it makes rendering results easier and allows us to have tests of differing lengths
# a problem here is where to store the solutions?
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # alphabet_test = db.relationship('AlphabetTest', backref='testee')

    def __repr__(self):
        return '<User {}>'.format(self.name)  
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_progress(self):
        alphabet_quiz_completed = AlphabetQuiz.query.filter_by(testee_id=self.id).first() is not None
        numbers_quiz_completed = NumbersQuiz.query.filter_by(testee_id=self.id).first() is not None
        # do for each quiz type
        quizzes = [alphabet_quiz_completed, numbers_quiz_completed]
        current_progress = round(sum([test == True for test in quizzes]) / len(quizzes) * 100)
        return current_progress

    def get_next_module(self):
        if AlphabetQuiz.query.filter_by(testee_id=self.id).first() is None:
            return "alphabet"
        if NumbersQuiz.query.filter_by(testee_id=self.id).first() is None:
            return "numbers"
        if GreetingsQuiz.query.filter_by(testee_id=self.id).first() is None:
            return "greetings"
        if ColoursQuiz.query.filter_by(testee_id=self.id).first() is None:
            return "colours"
        if ArticlesQuiz.query.filter_by(testee_id=self.id).first() is None:
            return "articles"
        if VerbsQuiz.query.filter_by(testee_id=self.id).first() is None:
            return "verbs"
        # elif go through each quiz in order
        return None

# class Quiz(db.Model):
    # id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

"""
How quiz answers are stored:
    answers from StringField questions are stored as strings.
    answers from IntegerField questions are stored as integers.
    answers from RadioField questions (represent multi-choice questions, where only one answer is allowed) 
        are stored as integers corresponding to the number of the selected option.
    answers from MultiCheckboxField questions (represent multi-choice questions, where zero to multiple 
        answers are allowed) are stored as binary strings where a 1 in the ith position denotes that the 
        ith option has been selected.
"""

class AlphabetQuiz(db.Model):
    """
    q1 IntegerField question
    q2 RadioField question
    q3 MultiCheckboxField question
    q4 MultiCheckboxField question
    """
    id = db.Column(db.Integer, primary_key=True)
    testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.String(4))
    q4 = db.Column(db.String(4))
    # the user's score for this quiz (between 0 and 1)
    score = db.Column(db.Float, nullable=True)

    def get_answers(self):
        return [self.q1, self.q2, self.q3, self.q4]

class NumbersQuiz(db.Model):
    """
    q1 RadioField question
    q2 StringField question
    q3 RadioField question
    q4 StringField question
    """
    id = db.Column(db.Integer, primary_key=True)
    testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.String(10))
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.String(10))
    score = db.Column(db.Float, nullable=True)

    def get_answers(self):
        return [self.q1, self.q2, self.q3, self.q4]

class GreetingsQuiz(db.Model):
    """
    q1 RadioField question
    q2 StringField question
    q3 RadioField question
    q4 StringField question
    """
    id = db.Column(db.Integer, primary_key=True)
    testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.String(20))
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.String(20))
    score = db.Column(db.Float, nullable=True)

    def get_answers(self):
        return [self.q1, self.q2, self.q3, self.q4]
    
class ColoursQuiz(db.Model):
    """
    q1 StringField question
    q2 RadioField question
    q3 StringField question
    q4 RadioField question
    """
    id = db.Column(db.Integer, primary_key=True)
    testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    q1 = db.Column(db.String(10))
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.String(10))
    q4 = db.Column(db.Integer)
    score = db.Column(db.Float, nullable=True)

    def get_answers(self):
        return [self.q1, self.q2, self.q3, self.q4]
    
class ArticlesQuiz(db.Model):
    """
    q1 RadioField question
    q2 RadioField question
    q3 RadioField question
    q4 StringField question
    q5 RadioField question
    q6 RadioField question
    q7 RadioField question
    q8 StringField question
    """
    id = db.Column(db.Integer, primary_key=True)
    testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.String(10))
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.String(10))
    score = db.Column(db.Float, nullable=True)

    def get_answers(self):
        return [self.q1, self.q2, self.q3, self.q4, self.q5, self.q6, self.q7, self.q8]

class VerbsQuiz(db.Model):
    """
    q1 RadioField question
    q2 StringField question
    q3 StringField question
    q4 RadioField question
    """
    id = db.Column(db.Integer, primary_key=True)
    testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.String(20))
    q3 = db.Column(db.String(20))
    q4 = db.Column(db.Integer)
    score = db.Column(db.Float, nullable=True)

    def get_answers(self):
        return [self.q1, self.q2, self.q3, self.q4]
