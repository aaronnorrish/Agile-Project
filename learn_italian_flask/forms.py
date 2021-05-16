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
