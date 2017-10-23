#!/usr/bin/env python
# -*- coding=utf-8 -*-

import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from markdown import markdown


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True, nullable=False)
    gravatar_url = db.Column(db.String(128))
    password_hash = db.Column(db.String(128), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.now())
    last_login_date = db.Column(db.DateTime, default=datetime.now())
    location = db.Column(db.String(128))
    about_me = db.Column(db.Text())
    articles = db.relationship('Article', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email and self.gravatar_url is None:
            self.gravatar_url = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def verify_password(hash, password):
        return check_password_hash(hash, password)

    def change_email(self, email):
        self.gravatar_url = hashlib.md5(email.encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://https://s.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.gravatar_url or \
            hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @staticmethod
    def add_users_date():
        """Add register and last login data after update db scheme"""
        users = User.query
        for user in users:
            if user.register_date is None:
                user.register_date = datetime.now()
            if user.last_login_date is None:
                user.last_login_date = datetime.now()
            db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


articles_tags = db.Table(
    'articles_tags',
    db.Column('tag_id', db.Integer,
              db.ForeignKey('tags.id'), primary_key=True),
    db.Column('article_id', db.Integer,
              db.ForeignKey('articles.id'), primary_key=True))


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text())
    markdown_html = db.Column(db.Text())
    create_timestramp = db.Column(db.DateTime, index=True,
                                  default=datetime.now())
    last_edit_timestramp = db.Column(db.DateTime, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                          nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),
                            nullable=False)
    tags = db.relationship('Tag', secondary=articles_tags, lazy='dynamic',
                           backref=db.backref('articles', lazy='dynamic'))
    number_of_views = db.Column(db.Integer, default=0)

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        target.markdown_html = markdown(
            value,
            ouput_format='html',
            extensions=['markdown.extensions.extra',
                        'markdown.extensions.admonition',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.headerid',
                        'markdown.extensions.meta',
                        'markdown.extensions.nl2br',
                        'markdown.extensions.sane_lists',
                        'markdown.extensions.smarty',
                        'markdown.extensions.toc',
                        'markdown.extensions.wikilinks',
                        'markdown.extensions.mathjax'])

    @staticmethod
    def add_one_view(article):
        article.number_of_views += 1
        db.session.add(article)
        db.session.commit()

    def __repr__(self):
        return '<Article %r>' % self.title


db.event.listen(Article.content, 'set', Article.on_changed_content)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self.name
