from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.utcnow())
    last_login_date = db.Column(db.DateTime, default=datetime.utcnow())

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def verify_password(hash, password):
        return check_password_hash(hash, password)

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
