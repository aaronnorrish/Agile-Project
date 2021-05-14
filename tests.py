import unittest
from learn_italian_flask import app, db
from learn_italian_flask.models import User, AlphabetQuiz, NumbersQuiz

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
        u = User(name='niska', email="test@testmail.com")
        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.get_progress(), 0)

        quiz = NumbersQuiz(testee_id=1, q1=1, q2="cinq", q3=3, q4="acht")
        db.session.add(quiz)
        db.session.commit()

        # TODO this value will change as we add more quizzes!
        self.assertEqual(u.get_progress(), 50)

        quiz = AlphabetQuiz(testee_id=1, q1=97, q2=1, q3="1111", q4="0000")
        db.session.add(quiz)
        db.session.commit()

        # TODO this value will change as we add more quizzes!
        self.assertEqual(u.get_progress(), 100)

    def test_get_next_module(self):
        u = User(name='niska', email="test@testmail.com")
        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.get_next_module(), "alphabet")

        quiz = NumbersQuiz(testee_id=1, q1=1, q2="cinq", q3=3, q4="acht")
        db.session.add(quiz)
        db.session.commit()
        self.assertEqual(u.get_next_module(), "alphabet")

        quiz = AlphabetQuiz(testee_id=1, q1=97, q2=1, q3="1111", q4="0000")
        db.session.add(quiz)
        db.session.commit()
        self.assertEqual(u.get_next_module(), None)
    
    # TODO QuizController tests!

if __name__ == '__main__':
    unittest.main(verbosity=2)