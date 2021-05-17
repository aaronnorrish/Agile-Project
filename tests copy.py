import os, unittest, time
from learn_italian_flask import app, db
from learn_italian_flask.models import User, Quiz, UserAnswer 
from learn_italian_flask.controllers import UserController, QuizController, ResultsController
from selenium import webdriver

class UserModelCase(unittest.TestCase):
    driver = None

    def setUp(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        #Using forward slash for mac
        chrome_driver_path = dir + "/chromedriver"
        self.driver = webdriver.Chrome(chrome_driver_path)

        if not self.driver:
            self.skipTest("Web browser not avaialable")
        
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
            db.create_all()
            #u = User(id=1, name='niska', email="test@testmail.com")
            #q1 = Quiz(id=1, name="q1 name", q1_text="question 1", q1_type="integer", q2_text="question 2", q2_type="radio", q2_choices="t;f", q3_text="question 3", q3_type="radio", q3_choices="1;2;3;4", q4_text="question 4", q4_type="radio", q4_choices="t;f", sol1="one", sol2="t", sol3="3", sol4="f")
            #q2 = Quiz(id=2, name="q2 name", q1_text="question 1", q1_type="integer", q2_text="question 2", q2_type="radio", q2_choices="t;f", q3_text="question 3", q3_type="radio", q3_choices="1;2;3;4", q4_text="question 4", q4_type="radio", q4_choices="t;f", sol1="one", sol2="t", sol3="3", sol4="f")
            #ua = UserAnswer(quiz_id=1, user_id=1, ans1="one", ans2="t", ans3="3", ans4="f", score=1.0)
            #self.driver.maximise_window()
            self.driver.get('http://127.0.0.1:5000/')

    
    def tearDown(self):
        if self.driver:
            self.driver.quit()
            db.session.remove()
            db.drop_all()

    
    def test_signup(self):
        #u = User(id=1, name='niska', email="test@testmail.com")
        #db.session.add(u)
        #u2 = User.query.get('niska')
        #self.assertEqual(u2.email, 'test@testmail.com', msg="user exists in database")
        self.driver.get('http://127.0.0.1:5000/signup')
        self.driver.implicitly_wait(10)
        name_field = self.driver.find_element_by_id('name')
        name_field.send_keys('niska')
        password_field = self.driver.find_element_by_id('password')
        password_field.send_keys('pword')
        password_confirm_field = self.driver.find_element_by_id('confirmPassword')
        password_confirm_field.send_keys('pword')
        time.sleep(1)
        self.driver.implicitly_wait(10)
        submit = self.driver.find_element_by_id('submit')
        submit.click()
    
    
    """

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
    
    
    def test_user_answers(self):
        # Add User Answers
        ua = UserAnswer(quiz_id=1, user_id=1, ans1="one", ans2="t", ans3="3", ans4="f", score=1.0)
        db.session.add(ua)
        db.session.commit()

        ans = ["one", "t", "3", "f"]

        self.assertEqual(ua.get_user_answers(), ans)
    

    # Tests for controllers.py
    """
    """
    def test_populate_form(self):
    
    
    def test_construct_solution(self):
    
    
    def test_retreve_answers(self):

    
    def test_calculate_quiz_score(self):

    
    def test_generate_quiz_form(self):


    def test_get_results(self):
    """


if __name__ == '__main__':
    unittest.main(verbosity=2)