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
    # test_quiz_id = db.Column(db.Integer, db.ForeignKey('test_quiz.id'), nullable=True)
    # alphabet_test = db.relationship('AlphabetTest', backref='testee')

    def __repr__(self):
        return '<User {}>'.format(self.name)  
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_progress(self):
        test_quiz_completed = TestQuiz.query.filter_by(testee_id=self.id).first() is not None
        # do for each quiz type
        quizzes = [test_quiz_completed]
        current_progress = round(sum([test == True for test in quizzes]) / len(quizzes) * 100)
        return current_progress

    def get_next_module(self):
        if TestQuiz.query.filter_by(testee_id=self.id).first() is None:
            return "alphabet"
        # elif go through each quiz in order

class TestQuiz(db.Model):
    # id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # integer corresponding to the choice selected
    q1 = db.Column(db.Integer)
    q1_correct = db.Column(db.Boolean)
    q2 = db.Column(db.String(64))
    q2_correct = db.Column(db.Boolean)
    score = db.Column(db.Float)

# class Quiz(db.Model):
    # id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

# class AlphabetQuiz(db.Model, Test):
# class AlphabetQuiz(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     testee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
#     q1 = db.Column(db.Integer)
#     q2 = db.Column(db.BOOLEAN)
#     q3 = db.Column(db.String(20))