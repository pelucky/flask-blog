from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, TextAreaField)
from wtforms.validators import DataRequired, EqualTo, Email


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


class ChangeUserInformationForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),
                        Email("Invalid Email")])
    about_me = TextAreaField('About_me', validators=[DataRequired()])
    submit = SubmitField('Submit')
