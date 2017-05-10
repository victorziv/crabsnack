from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, SubmitField,
    TextAreaField, Email, Regexp, SelectField)

from wtforms.validators import DataRequired, Required, Length
from ..models import Role, User


class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

# ===============================


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
# ===============================


class EditProfileForm(FlaskForm):
    username = StringField('User name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
# ===============================


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField(
        'Username',
        validators=[
            Required(),
            Length(1, 64),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')
        ])

    confirmed = BooleanField('Confirmed'),
    role = SelectField('Role', coerce=int)
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
    # _________________________________

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user
    # _________________________________

    def validate_email(self, field):
        if field.data != self.user.email and User().find_one_by_field(name='email', value=field.data):
            raise ValidationError('Email already registered.')
    # _________________________________

    def validate_username(self, field):
        if field.data != self.user.username and User().query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
