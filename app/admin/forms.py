#!/usr/bin/env python
# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, TextAreaField, SelectField)
from wtforms.validators import DataRequired, EqualTo, Email, length
from ..models import Category


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


class WriteArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(max=255)])
    category_id = SelectField('Categories', coerce=int)
    tags = StringField('Tag', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

    def __init__(self):
        super(WriteArticleForm, self).__init__()
        self.category_id.choices = [(c.id, c.name)
                                    for c in Category.query.order_by('id')]


class AddCategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditCategoryForm(FlaskForm):
    category_id = SelectField('Categories', coerce=int)
    new_name = StringField('Category new name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self):
        super(EditCategoryForm, self).__init__()
        self.category_id.choices = [(c.id, c.name)
                                    for c in Category.query.order_by('id')]


class DeleteCategoryForm(FlaskForm):
    category_id = SelectField('Categories', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(DeleteCategoryForm, self).__init__()
        self.category_id.choices = [(c.id, c.name)
                                    for c in Category.query.order_by('id')]


class EditTagForm(FlaskForm):
    old_name = StringField('Tag old name', validators=[DataRequired()])
    new_name = StringField('Tag new name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeleteTagForm(FlaskForm):
    tag_name = StringField('Tag name', validators=[DataRequired()])
    submit = SubmitField('Submit')
