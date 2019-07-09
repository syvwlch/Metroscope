"""Define the forms for the auth blueprint."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    """Define the login form."""
    email = StringField(
        'Email',
        validators=[DataRequired(), Length(1, 64), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
