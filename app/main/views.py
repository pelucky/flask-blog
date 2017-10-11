from flask import render_template
from ..models import User
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/about_me')
def about_me():
    user = User.query.filter_by(id=1).first()
    return render_template('about_me.html', user=user)
