import unittest
from learn_italian_flask import app, db
from learn_italian_flask.models import User, Quiz, UserAnswer 
from learn_italian_flask.controllers import _populate_form, _construct_solution, _retrieve_answers, _calculate_quiz_score, _generate_quiz_form

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(name='niska', email="test@testmail.com")
        u.set_password('chiave')
        self.assertFalse(u.check_password('chiavi'))
        self.assertTrue(u.check_password('chiave'))

    def test_get_progress(self):
        u = User(id=1, name='niska', email="test@testmail.com")
        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.get_progress(), 0)
        
        # Add Quiz
        q = Quiz(id=1, name="q1 name", q1_text="question 1", q1_type="integer", q2_text="question 2", q2_type="radio", q2_choices="t;f", q3_text="question 3", q3_type="radio", q3_choices="1;2;3;4", q4_text="question 4", q4_type="radio", q4_choices="t;f", sol1="one", sol2="t", sol3="3", sol4="f")
        db.session.add(q)
        db.session.commit()

        # Add User Answers
        ua = UserAnswer(quiz_id=1, user_id=1, ans1="one", ans2="t", ans3="3", ans4="f", score=1.0)
        db.session.add(ua)
        db.session.commit()

        self.assertEqual(u.get_progress(), 100)

        # Add Quiz
        q2 = Quiz(id=2, name="q2 name", q1_text="question 1", q1_type="integer", q2_text="question 2", q2_type="radio", q2_choices="t;f", q3_text="question 3", q3_type="radio", q3_choices="1;2;3;4", q4_text="question 4", q4_type="radio", q4_choices="t;f", sol1="one", sol2="t", sol3="3", sol4="f")
        db.session.add(q2)
        db.session.commit()

        self.assertEqual(u.get_progress(), 50)


    def test_get_next_module(self):
        u = User(id=1, name='niska', email="test@testmail.com")
        db.session.add(u)
        db.session.commit()

        # Add Quiz
        q1 = Quiz(id=1, name="q1 name", q1_text="question 1", q1_type="integer", q2_text="question 2", q2_type="radio", q2_choices="t;f", q3_text="question 3", q3_type="radio", q3_choices="1;2;3;4", q4_text="question 4", q4_type="radio", q4_choices="t;f", sol1="one", sol2="t", sol3="3", sol4="f")
        q2 = Quiz(id=2, name="q2 name", q1_text="question 1", q1_type="integer", q2_text="question 2", q2_type="radio", q2_choices="t;f", q3_text="question 3", q3_type="radio", q3_choices="1;2;3;4", q4_text="question 4", q4_type="radio", q4_choices="t;f", sol1="one", sol2="t", sol3="3", sol4="f")
        db.session.add_all([q1, q2])
        db.session.commit()

        # Add User Answers
        ua = UserAnswer(quiz_id=1, user_id=1, ans1="one", ans2="t", ans3="3", ans4="f", score=1.0)
        db.session.add(ua)
        db.session.commit()

        self.assertEqual(u.get_next_module(), "q2 name")

        # Add User Answers
        ua2 = UserAnswer(quiz_id=2, user_id=1, ans1="one", ans2="t", ans3="3", ans4="f", score=1.0)
        db.session.add(ua2)
        db.session.commit()

        self.assertEqual(u.get_next_module(), None)

class QuizModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_questions(self):
        q = Quiz(id=1, name="q1 name", q1_text="question 1", q1_type="integer", q2_text="question 2", q2_type="radio", q2_choices="t;f", q3_text="question 3", q3_type="radio", q3_choices="1;2;3;4", q4_text="question 4", q4_type="radio", q4_choices="t;f", sol1="one", sol2="t", sol3="3", sol4="f")
        db.session.add(q)
        db.session.commit()

        qns = {
            "question1": {
                "text": "question 1",
                "type": "integer",
                "choices": []
            },
            "question2": {
                "text": "question 2",
                "type": "radio",
                "choices": [('0', 't'), ('1', 'f')]
            },
            "question3": {
                "text": "question 3",
                "type": "radio",
                "choices": [('0', '1'), ('1', '2'), ('2','3'), ('3', '4')]
            },
            "question4": {
                "text": "question 4",
                "type": "radio",
                "choices": [('0', 't'), ('1', 'f')]
            }
        }

        self.assertEqual(q.get_questions(), qns)


    def test_get_solutions(self):
        # Add Quiz
        q = Quiz(id=1, name="q1 name", q1_text="question 1", q1_type="integer", q2_text="question 2", q2_type="radio", q2_choices="t;f", q3_text="question 3", q3_type="radio", q3_choices="1;2;3;4", q4_text="question 4", q4_type="radio", q4_choices="t;f", sol1="one", sol2="t", sol3="3", sol4="f")
        db.session.add(q)
        db.session.commit()

        soln = ["one", "t", "3", "f"]

        self.assertEqual(q.get_solutions(), soln)

class UserAnswersModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_user_answers(self):
        # Add User Answers
        ua = UserAnswer(quiz_id=1, user_id=1, ans1="one", ans2="t", ans3="3", ans4="f", score=1.0)
        db.session.add(ua)
        db.session.commit()

        ans = ["one", "t", "3", "f"]

        self.assertEqual(ua.get_user_answers(), ans)
    
    """

    # Tests for controllers.py
    
    def test_populate_form(self):
    
    
    def test_construct_solution(self):
    
    
    def test_retreve_answers(self):

    
    def test_calculate_quiz_score(self):

    
    def test_generate_quiz_form(self):


    def test_get_results(self):
]

    """

class ControllerHelpersCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

        quiz1 = Quiz(name="Numbers",
        q1_text="Quattro is which number in Italian?",
        q1_type="Radio",
        q1_choices="one;two;three;four",
        q2_text='Write "five" in Italian:',
        q2_type="String",
        q3_text="What is seven in Italian?",
        q3_type="Radio",
        q3_choices="tre;uno;sei;sette",
        q4_type="String",
        q4_text="Complete this sequence: sei, sette, __, nove",
        sol1="3",
        sol2="cinque",
        sol3="3",
        sol4="otto"
        )

        quiz2 = Quiz(name="Colours",
        q1_text='Write "orange" in Italian:',
        q1_type="String",
        q2_text='What colour is "rosa" in English:',
        q2_type="Radio",
        q2_choices="red;pink",
        q3_text="What is the Italian word for blue?",
        q3_type="String",
        q4_text="Which of the following translates to black?",
        q4_type="Radio",
        q4_choices="bianco;verde;nero;giallo",
        sol1="arancione",
        sol2="1",
        sol3="blu",
        sol4="2"
        )

        db.session.add_all([quiz1, quiz2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_calculate_score(self):
        user_answers1 = {'answer1': {'type': 'RadioField', 'value': '3'}, 
                         'answer2': {'type': 'StringField', 'value': 'hello'}, 
                         'answer3': {'type': 'RadioField', 'value': '1'}, 
                         'answer4': {'type': 'StringField', 'value': 'asd'}}

        numbers_solutions = Quiz.query.filter_by(name="Numbers").first().get_solutions()
        score = _calculate_quiz_score(user_answers1, numbers_solutions)
        self.assertEqual(score, 0.25)

        user_answers2 = {'answer1': {'type': 'StringField', 'value': 'naranja'}, 
                        'answer2': {'type': 'RadioField', 'value': '1'}, 
                        'answer3': {'type': 'StringField', 'value': 'blu'}, 
                        'answer4': {'type': 'RadioField', 'value': '1'}}
        
        colours_solutions = Quiz.query.filter_by(name="Colours").first().get_solutions()
        score = _calculate_quiz_score(user_answers2, colours_solutions)
        self.assertEqual(score, 0.5)


if __name__ == '__main__':
    unittest.main(verbosity=2)