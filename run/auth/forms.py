"""Define the forms for the auth blueprint."""

from flask_wtf import FlaskForm, RecaptchaField
from ..models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class LoginForm(FlaskForm):
    """Define the login form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email(),
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email(),
        ],
    )
    display_name = StringField(
        'Display Name',
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$',
                0,
                'Display names must have only letters, numbers, dots or '
                'underscores'),
        ],
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('password2', message='Passwords must match.'),
        ],
    )
    password2 = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_display_name(self, field):
        if User.query.filter_by(display_name=field.data).first():
            raise ValidationError('Display name already in use.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        'Old password',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'New password',
        validators=[
            DataRequired(),
            EqualTo('password2', message='Passwords must match.'),
        ],
    )
    password2 = PasswordField(
        'Confirm new password',
        validators=[DataRequired()],
    )
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email(),
        ],
    )
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            EqualTo('password2', message='Passwords must match'),
        ],
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()],
    )
    submit = SubmitField('Reset Password')
