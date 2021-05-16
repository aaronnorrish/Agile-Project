from learn_italian_flask import app
from learn_italian_flask import db
from learn_italian_flask.models import User, Quiz, UserAnswer

quiz1 = Quiz(name="Alphabet",
q1_text="There are __ letters in the Italian Alphabet:",
q1_type="Integer",
q2_text="The letter W is in the Italian Alphabet.",
q2_type="Radio",
q2_choices="True;False",
q3_text="Which of the following letters are in the Italian Alphabet?",
q3_type="Checkbox",
q3_choices="a;s;d;y",
q4_text="Which of the following letters are NOT in the Italian Alphabet?",
q4_type="Checkbox",
q4_choices="j;q;u;z",
sol1="21",
sol2="1",
sol3="1110",
sol4="1000"
)

quiz2 = Quiz(name="Numbers",
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

quiz3 = Quiz(name="Greetings",
q1_text="Buongiorno means Good Evening?",
q1_type="Radio",
q1_choices="True;False",
q2_text='Write "good night" in Italian:',
q2_type="String",
q3_text='What is "how are you" in Italian?',
q3_type="Radio",
q3_choices="Ciao;Come stai",
q4_text="What is Buon pomeriggio in English?",
q4_type="String",
sol1="1",
sol2="Buonanotte",
sol3="0",
sol4="Good afternoon"
)

quiz4 = Quiz(name="Colours",
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

quiz5 = Quiz(name="Articles",
q1_text="Which of the following options would precede zio?",
q1_type="Radio",
q1_choices="il;lo;l'",
q2_text="Which of the following options would precede gatto?",
q2_type="Radio",
q2_choices="il;lo;l'",
q3_text="Which of the following options would precede casa?",
q3_type="Radio",
q3_choices="la;l'",
q4_text="Insert the correct definite article: __ studente",
q4_type="String",
q5_text="Which of the following options would precede palla?",
q5_type="Radio",
q5_choices="una;un'",
q6_text="Which of the following options would precede isola?",
q6_type="Radio",
q6_choices="una;un'",
q7_text="Which of the following options would precede zaino?",
q7_type="Radio",
q7_choices="un;uno",
q8_text="Insert the correct indefinite article: __ macchina",
q8_type="String",
sol1="1",
sol2="0",
sol3="0",
sol4="lo",
sol5="0",
sol6="1",
sol7="1",
sol8="una"
)

quiz6 = Quiz(name="Verbs",
q1_text='Mangiare means "to eat?"',
q1_type="Radio",
q1_choices="True;False",
q2_text='Write "to know" in Italian:',
q2_type="String",
q3_text="What is mettere in English",
q3_type="String",
q4_text='What is "to speak" in Italian?',
q4_type="Radio",
q4_choices="avere;volere;parlare;sentire",
sol1="0",
sol2="sapere",
sol3="to put",
sol4="2"
)

db.session.add_all([quiz1, quiz2, quiz3, quiz4, quiz5, quiz6])
db.session.commit()

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