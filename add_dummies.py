from learn_italian_flask import app
from learn_italian_flask import db
from learn_italian_flask.models import User, Quiz, UserAnswer


user1 = User(
    name="niska",
    email="niska@testmail.com"
)
user1.set_password("niska")

user2 = User(
    name="damso",
    email="damso@testmail.com"
)
user2.set_password("damso")

db.session.add_all([user1, user2])
db.session.commit()

answer1 = UserAnswer(
    quiz_id=1,
    user_id=1,
    ans1="21",
    ans2='0',
    ans3='1100',
    ans4='0110',
    score=0.5
)

answer2 = UserAnswer(
    quiz_id=2,
    user_id=1,
    ans1="3",
    ans2="cinque",
    ans3="3",
    ans4="otto",
    score=1.0
)

answer3 = UserAnswer(
    quiz_id=3,
    user_id=1,
    ans1="1",
    ans2="gut nacht",
    ans3="1",
    ans4="Good afternoon",
    score=0.75
)

answer4 = UserAnswer(
    quiz_id=2,
    user_id=2,
    ans1="3",
    ans2="cinque",
    ans3="3",
    ans4="acht",
    score=0.75
)

answer5 = UserAnswer(
    quiz_id=4,
    user_id=2,
    ans1="arancione",
    ans2="1",
    ans3="blau",
    ans4="1",
    score=0.5
)

db.session.add_all([answer1, answer2, answer3, answer4, answer5])
db.session.commit()