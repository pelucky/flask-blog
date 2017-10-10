from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField)
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password',
                                 validators=[DataRequired()])
    password = PasswordField('New Password',
                             validators=[DataRequired()])
    confirm = PasswordField(
        'Repeat Password',
        validators=[DataRequired(),
                    EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')
