import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True, nullable=False)
    gravatar_url = db.Column(db.String(128))
    password_hash = db.Column(db.String(128), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.utcnow())
    last_login_date = db.Column(db.DateTime, default=datetime.utcnow())
    location = db.Column(db.String(128))
    about_me = db.Column(db.Text())

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
                user.register_date = datetime.utcnow()
            if user.last_login_date is None:
                user.last_login_date = datetime.utcnow()
            db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
