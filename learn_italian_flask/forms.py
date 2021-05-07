from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
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
    confirmPassword = PasswordField('Password confirmation', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email has already been used.')

class TestQuizForm(FlaskForm):
    # question1 = RadioField("Choose the correct option:", choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')], validators=[DataRequired()], render_kw={'disabled':'false'})
    question1 = RadioField("Choose the correct option:", choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')], validators=[DataRequired()])
    # question2 = StringField("Enter:", validators=[DataRequired()], render_kw={'disabled':'false'})
    question2 = StringField("Enter:", validators=[DataRequired()])
    # submit = SubmitField('Submit Answers!', render_kw={'disabled':'false'})
    submit = SubmitField('Submit Answers!')

from wtforms import widgets, SelectMultipleField

class MultiCheckboxField(SelectMultipleField):
    """
    Helper class for rendering multiple checkboxes within one field.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AlphabetQuizForm(FlaskForm):
    question1 = StringField("There are __ letters in the Italian Alphabet:", validators=[DataRequired()])
    question2 = RadioField("The letter W is in the Italian Alphabet.", choices=[('1', 'True'), ('2', 'False')], validators=[DataRequired()])
    question3 = MultiCheckboxField("Which of the following letters are in the Italian Alphabet?", choices=[("0", "a"), ("1", "s"), ("2", "d"), ("3", "y")])
    question4 = MultiCheckboxField("Which of the following letters are NOT in the Italian Alphabet?", choices=[("0", "j"), ("1", "q"), ("2", "u"), ("3", "z")])
    submit = SubmitField('Submit Answers!')

class NumbersQuizForm(FlaskForm):
    question1 = RadioField("Quattro is which number in Italian?", choices=[('one'), ('two'), ('three'), ('four')], validators=[DataRequired()])
    question2 = StringField('Write "five" in Italian:', validators=[DataRequired()])
    question3 = RadioField("What is seven in Italian?", choices=[('tre'), ('uno'), ('sei'), ('sette')], validators=[DataRequired()])
    question4 = StringField("Complete this sequence: sei, sette, __, nove", validators=[DataRequired()])
    submit = SubmitField('Submit Answers!')