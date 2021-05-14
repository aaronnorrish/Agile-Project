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

    def __repr__(self):
        return '<User {}>'.format(self.name)  
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_progress(self):
        # determine the number of quizzes the current user has completed
        user_quizzes = UserAnswer.query.filter_by(user_id=self.id)
        num_completed = 0
        if user_quizzes is not None:
            num_completed = sum([1 for quiz in user_quizzes])

        # determine the total number of quizzes
        total_quizzes = 1 # to avoid division by zero
        all_quizzes = Quiz.query.all()
        if all_quizzes is not None:
            total_quizzes = sum([1 for quiz in all_quizzes])
        
        current_progress = round(num_completed/total_quizzes * 100)
        return current_progress

    def get_next_module(self):
        user_quizzes = UserAnswer.query.filter_by(user_id=self.id)
        completed_quiz_ids = [quiz.quiz_id for quiz in user_quizzes]
        all_quizzes = Quiz.query.all()
        for quiz in all_quizzes:
            if quiz.id not in completed_quiz_ids:
                return quiz.name
        return None

class Quiz(db.Model):
    # a quiz needs to have at least 4 questions
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    q1_text = db.Column(db.String(20))
    q1_type = db.Column(db.String(10))
    q1_choices= db.Column(db.String(40), nullable=True)
    q2_text = db.Column(db.String(20))
    q2_type = db.Column(db.String(10))
    q2_choices= db.Column(db.String(40), nullable=True)
    q3_text = db.Column(db.String(20))
    q3_type = db.Column(db.String(10))
    q3_choices= db.Column(db.String(40), nullable=True)
    q4_text = db.Column(db.String(20))
    q4_type = db.Column(db.String(10))
    q4_choices= db.Column(db.String(40), nullable=True)
    q5_text = db.Column(db.String(20), nullable=True)
    q5_type = db.Column(db.String(10), nullable=True)
    q5_choices= db.Column(db.String(40), nullable=True)
    q6_text = db.Column(db.String(20), nullable=True)
    q6_type = db.Column(db.String(10), nullable=True)
    q6_choices= db.Column(db.String(40), nullable=True)
    q7_text = db.Column(db.String(20), nullable=True)
    q7_type = db.Column(db.String(10), nullable=True)
    q7_choices = db.Column(db.String(40), nullable=True)
    q8_text = db.Column(db.String(20), nullable=True)
    q8_type = db.Column(db.String(10), nullable=True)
    q8_choices= db.Column(db.String(40), nullable=True)
    sol1 = db.Column(db.String(20))
    sol2 = db.Column(db.String(20))
    sol3 = db.Column(db.String(20))
    sol4 = db.Column(db.String(20))
    sol5 = db.Column(db.String(20))
    sol5 = db.Column(db.String(20))
    sol6 = db.Column(db.String(20))
    sol7 = db.Column(db.String(20))
    sol8 = db.Column(db.String(20))

    def get_questions(self):
        questions = {
            "question1": {
                "text": self.q1_text,
                "type": self.q1_type,
                "choices": [(str(i), choice) for i, choice in zip(range(len(self.q1_choices.split(";"))), self.q1_choices.split(";"))] if self.q1_choices else []
            },
            "question2": {
                "text": self.q2_text,
                "type": self.q2_type,
                "choices": [(str(i), choice) for i, choice in zip(range(len(self.q2_choices.split(";"))), self.q2_choices.split(";"))] if self.q2_choices else []
            },
            "question3": {
                "text": self.q3_text,
                "type": self.q3_type,
                "choices": [(str(i), choice) for i, choice in zip(range(len(self.q3_choices.split(";"))), self.q3_choices.split(";"))] if self.q3_choices else []
            },
            "question4": {
                "text": self.q4_text,
                "type": self.q4_type,
                "choices": [(str(i), choice) for i, choice in zip(range(len(self.q4_choices.split(";"))), self.q4_choices.split(";"))] if self.q4_choices else []
            }
        }
        if self.q5_text:
            questions["question5"] = {
                "text": self.q5_text,
                "type": self.q5_type,
                "choices": [(str(i), choice) for i, choice in zip(range(len(self.q5_choices.split(";"))), self.q5_choices.split(";"))] if self.q5_choices else []
            }
        if self.q6_text:
            questions["question6"] = {
                "text": self.q6_text,
                "type": self.q6_type,
                "choices": [(str(i), choice) for i, choice in zip(range(len(self.q6_choices.split(";"))), self.q6_choices.split(";"))] if self.q6_choices else []
            }
        if self.q7_text:
            questions["question7"] = {
                "text": self.q7_text,
                "type": self.q7_type,
                "choices": [(str(i), choice) for i, choice in zip(range(len(self.q7_choices.split(";"))), self.q7_choices.split(";"))] if self.q7_choices else []
            }
        if self.q8_text:
            questions["question8"] = {
                "text": self.q8_text,
                "type": self.q8_type,
                "choices": [(str(i), choice) for i, choice in zip(range(len(self.q8_choices.split(";"))), self.q8_choices.split(";"))] if self.q8_choices else []
            }
        return questions

    def get_solutions(self):
        solutions = [self.sol1, self.sol2, self.sol3, self.sol4]
        if self.sol5:
            solutions.append(self.sol5)
        if self.sol6:
            solutions.append(self.sol6)
        if self.sol7:
            solutions.append(self.sol7)
        if self.sol8:
            solutions.append(self.sol8)
        return solutions

class UserAnswer(db.Model):
    quiz_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    ans1 = db.Column(db.String(20))
    ans2 = db.Column(db.String(20))
    ans3 = db.Column(db.String(20))
    ans4 = db.Column(db.String(20))
    ans5 = db.Column(db.String(20))
    ans5 = db.Column(db.String(20), nullable=True)
    ans6 = db.Column(db.String(20), nullable=True)
    ans7 = db.Column(db.String(20), nullable=True)
    ans8 = db.Column(db.String(20), nullable=True)
    score = db.Column(db.Float)

    def get_user_answers(self):
        user_answers = [self.ans1, self.ans2, self.ans3, self.ans4]
        if self.ans5:
            user_answers.append(self.ans5)
        if self.ans6:
            user_answers.append(self.ans6)
        if self.ans7:
            user_answers.append(self.ans7)
        if self.ans8:
            user_answers.append(self.ans8)
        return user_answers

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

