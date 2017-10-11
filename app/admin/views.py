from flask import render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import admin
from forms import LoginForm, ChangePasswordForm, ChangeUserInformationForm
from ..models import User
from app import db
from datetime import datetime


@admin.route('/', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.verify_password(user.password_hash,
                                             form.password.data):
                login_user(user, remember=form.remember_me.data)
                user.last_login_date = datetime.utcnow()
                flash("Log in successfully!")
                return redirect(url_for('admin.index'))
            flash("Username or Password error!")
        return render_template('admin/login.html', form=form)
    return redirect(url_for('admin.index'))


@admin.route('/index')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Log out successfully!")
    return redirect(url_for('main.index'))


@admin.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user and current_user.verify_password(
                current_user.password_hash, form.old_password.data):
            current_user.password = form.password.data
            flash("Change password successfully!")
            return redirect(url_for('admin.index'))
        flash("Old Password error!")
    return render_template('admin/change_password.html', form=form)


@admin.route('/change_user_info', methods=['GET', 'POST'])
@login_required
def change_user_info():
    form = ChangeUserInformationForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        print "form.nickname.data: " + form.nickname.data
        if current_user.email != form.email.data:
            current_user.change_email(form.email.data)
            current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash("Change user infomation successfully!")
        return redirect(url_for('main.about_me'))
    form.nickname.data = current_user.nickname
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.email.data = current_user.email
    return render_template('admin/change_user_info.html', form=form)
