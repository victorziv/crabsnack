from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

# ====================================


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
# ====================================


class RegistrationForm(FlaskForm):

    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField(
        'Username',
        validators=[
            Required(),
            Length(1, 64),
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$', 0,
                'Usernames must have only letters, numbers, dots or underscores'
            )
        ]
    )

    password = PasswordField(
        'Password',
        validators=[Required(), EqualTo('password2', message='Passwords must match.')])

    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')
    # _____________________________

    def validate_email(self, field):
        um = User()
        if um.exists_by_email(email=field.data):
            raise ValidationError('Email already registered.')

    # _____________________________

    def validate_username(self, field):
        um = User()
        if um.exists_by_username(username=field.data):
            raise ValidationError('Username already in use.')
