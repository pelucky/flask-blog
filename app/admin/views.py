from flask import render_template, url_for, redirect, flash
from . import admin
from forms import LoginForm


@admin.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Log in successfully")
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/index')
def index():
    pass
