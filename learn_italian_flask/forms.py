from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectMultipleField, widgets
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length, NumberRange
from learn_italian_flask.models import User

class LoginForm(FlaskForm):
    # in the flask tute they add as a string field and use an email validator
    # TODO using browser validation so might be able to get rid of validators?
    #       maybe not because client could just remove the HTML?
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Password confirmation', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email has already been used.')

class MultiCheckboxField(SelectMultipleField):
    """
    Helper class for rendering multiple checkboxes within one field.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AlphabetQuizForm(FlaskForm):
    question1 = IntegerField("There are __ letters in the Italian Alphabet:", validators=[DataRequired(), NumberRange(min=0,max=999)])
    question2 = RadioField("The letter W is in the Italian Alphabet.", choices=[('0', 'True'), ('1', 'False')], validators=[DataRequired()])
    question3 = MultiCheckboxField("Which of the following letters are in the Italian Alphabet?", choices=[("0", "a"), ("1", "s"), ("2", "d"), ("3", "y")])
    question4 = MultiCheckboxField("Which of the following letters are NOT in the Italian Alphabet?", choices=[("0", "j"), ("1", "q"), ("2", "u"), ("3", "z")])
    submit = SubmitField('Submit Answers!')

class NumbersQuizForm(FlaskForm):
    question1 = RadioField("Quattro is which number in Italian?", choices=[('0', 'one'), ('1', 'two'), ('2', 'three'), ('3','four')], validators=[DataRequired()])
    question2 = StringField('Write "five" in Italian:', validators=[DataRequired(), Length(max=10)])
    question3 = RadioField("What is seven in Italian?", choices=[('0', 'tre'), ('1', 'uno'), ('2', 'sei'), ('3', 'sette')], validators=[DataRequired()])
    question4 = StringField("Complete this sequence: sei, sette, __, nove", validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Submit Answers!')

class GreetingsQuizForm(FlaskForm):
    question1 = RadioField("Buon Giorno means Good Evening?", choices=[('0', 'True'), ('1', 'False')], validators=[DataRequired()])
    question2 = StringField('Write "good night" in Italian:', validators=[DataRequired(), Length(max=20)])
    question3 = RadioField("What is 'how are you' in Italian?", choices=[('0', 'ciao'), ('1', 'come stai')], validators=[DataRequired()])
    question4 = StringField("What is Good Night in Italian", validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit Answers!')

class ColoursQuizForm(FlaskForm):
    question1 = StringField('Write "orange" in Italian:', validators=[DataRequired(), Length(max=10)])
    question2 = RadioField("What is rosa in English?", choices=[('0', 'red'), ('1', 'pink')], validators=[DataRequired()])
    question3 = StringField("What is the Italian word for Blue?", validators=[DataRequired(), Length(max=10)])
    question4 = RadioField("Which of the following translates to black?", choices=[('0', 'bianco'), ('1', 'verde'), ('2', 'nero'), ('3','giallo')], validators=[DataRequired()])
    submit = SubmitField('Submit Answers!')

class ArticlesQuizForm(FlaskForm):
    question1 = RadioField("Which of the following options would precede zio?", choices=[('0', 'il'), ('1', 'lo'), ('2','l')], validators=[DataRequired()])
    question2 = RadioField("Which of the following options would precede gatti?", choices=[('0', 'il'), ('1', 'lo'), ('2','l')], validators=[DataRequired()])
    question3 = RadioField("Which of the following options would precede casa?", choices=[('0', 'la'), ('1', "l'")], validators=[DataRequired()])
    question4 = StringField("Insert the correct definite article: __ studente", validators=[DataRequired(), Length(max=10)])
    question5 = RadioField("Which of the following options would precede palla?", choices=[('0', 'una'), ('1', "un'")], validators=[DataRequired()])
    question6 = RadioField("Which of the following options would precede isola?", choices=[('0', 'una'), ('1', "un'")], validators=[DataRequired()])
    question7 = RadioField("Which of the following options would precede zaino?", choices=[('0', 'un'), ('1', 'uno')], validators=[DataRequired()])
    question8 = StringField("Insert the correct indefinite article: __ macchina", validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Submit Answers!')

class VerbsQuizForm(FlaskForm):
    question1 = RadioField("Mangiare means to eat?", choices=[('0', 'True'), ('1', 'False')], validators=[DataRequired()])
    question2 = StringField('Write "to know" in Italian:', validators=[DataRequired(), Length(max=20)])
    question3 = StringField("What is mettere in English", validators=[DataRequired(), Length(max=20)])
    question4 = RadioField("What is 'to speak' in Italian?", choices=[('0', 'avere'), ('1', 'volere'), ('2', 'parlare'), ('3','sentire')], validators=[DataRequired()])
    submit = SubmitField('Submit Answers!')