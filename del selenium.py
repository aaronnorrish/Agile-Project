import os, unittest, time
from learn_italian_flask import app, db
from learn_italian_flask.models import User, Quiz, UserAnswer 
from learn_italian_flask.controllers import UserController, QuizController, ResultsController
from selenium import webdriver
from flask import Flask
from flask_testing import LiveServerTestCase
from urllib.request import urlopen


class TestServer(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 500
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app
    
    def get_server(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


class UserModelCase(unittest.TestCase):
    driver = None

    def create_app(self):
        app = Flask(__name__)
        return app


    def setUp(self):
        self.app = self.create_app()
        app.config.update(
            # Specify the test database
            SQLALCHEMY_DATABASE_URI='sqlite://',
            # Change the port that the liveserver listens on
            LIVESERVER_PORT=5000
        )

        dir = os.path.dirname(os.path.abspath(__file__))
        #Using forward slash for mac
        chrome_driver_path = dir + "/chromedriver"
        self.driver = webdriver.Chrome(chrome_driver_path)
        self.driver.get(self.get_server_url())


        """
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
            self.driver.maximise_window()
            self.driver.get('http://127.0.0.1:5000/')
        """
    
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
        self.driver.get(self.get_server_url()+'/signup')
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

if __name__ == '__main__':
    unittest.main(verbosity=2)
    