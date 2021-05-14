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

class QuizForm(FlaskForm):
    submit = SubmitField('Submit Answers!')

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