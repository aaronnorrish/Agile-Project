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
    id = db.Column(db.Integer, primary_key=True)
    testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    q1 = db.Column(db.Integer)
    # integer corresponding to choice selected
    q2 = db.Column(db.Integer)
    # binary string corresponding to which options were selected
    # bin_string[0] == the first option
    q3 = db.Column(db.String(4))
    # binary string corresponding to which options were selected
    q4 = db.Column(db.String(4))
    # the user's score for this quiz (between 0 and 1)
    score = db.Column(db.Float, nullable=True)

    def get_answers(self):
        return [self.q1, self.q2, self.q3, self.q4]

class NumbersQuiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # integer corresponding to choice selected
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.String(10))
    # integer corresponding to choice selected
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.String(10))
    score = db.Column(db.Float, nullable=True)

    def get_answers(self):
        return [self.q1, self.q2, self.q3, self.q4]
