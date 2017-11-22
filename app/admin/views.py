#!/usr/bin/env python
# -*- coding=utf-8 -*-

from flask import (render_template, url_for,
                   redirect, flash, current_app, session, request)
from flask_login import login_user, login_required, logout_user, current_user
from . import admin
from forms import (LoginForm, ChangePasswordForm, ChangeUserInformationForm,
                   WriteArticleForm, AddCategoryForm, EditCategoryForm,
                   DeleteCategoryForm, EditTagForm, DeleteTagForm)
from ..models import User, Article, Category, Tag
from app import db
from datetime import datetime
import re
import random
from geetest import GeetestLib


@admin.route('/', methods=['GET'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        return render_template('admin/login.html', form=form)
    return redirect(url_for('admin.index'))


@admin.route('/geetest/register', methods=["GET"])
def get_captcha():
    geetest_user_id = random.randint(1, 100)
    gt = GeetestLib(current_app.config['GEETEST_ID'],
                    current_app.config['GEETEST_KEY'])
    status = gt.pre_process(geetest_user_id)
    session[gt.GT_STATUS_SESSION_KEY] = status
    session["geetest_user_id"] = geetest_user_id
    response_str = gt.get_response_str()
    return response_str


@admin.route('/geetest/validate', methods=["POST"])
def validate_captcha():
    gt = GeetestLib(current_app.config['GEETEST_ID'],
                    current_app.config['GEETEST_KEY'])
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]
    geetest_user_id = session["geetest_user_id"]
    if status:
        result = gt.success_validate(challenge, validate,
                                     seccode, geetest_user_id)
    else:
        result = gt.failback_validate(challenge, validate, seccode)
    form = LoginForm()
    if result & form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(user.password_hash,
                                         form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(u"Log in successfully! Your last login date is: %s"
                  % str(current_user.last_login_date).split('.')[0],
                  'success')
            user.last_login_date = datetime.now()
            return redirect(url_for('admin.index'))
        flash(u"Username or Password error!", 'error')
        current_app.logger.warning(u'Invalid Login: %s, %s'
                                   % (form.username.data,
                                      form.password.data))
    return render_template('admin/login.html', form=form)


@admin.route('/index')
@login_required
def index():
    articles = Article.query.order_by(Article.create_timestramp.desc())
    return render_template('admin/index.html', articles=articles)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u"Log out successfully!", 'success')
    return redirect(url_for('main.index'))


@admin.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user and current_user.verify_password(
                current_user.password_hash, form.old_password.data):
            current_user.password = form.password.data
            flash(u"Change password successfully!", 'success')
            return redirect(url_for('admin.index'))
        flash(u"Old Password error!", 'error')
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
        flash(u"Change user infomation successfully!", 'success')
        return redirect(url_for('main.about_me'))
    form.nickname.data = current_user.nickname
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.email.data = current_user.email
    return render_template('admin/change_user_info.html', form=form)


@admin.route('/write_article', methods=['GET', 'POST'])
@login_required
def write_article():
    form = WriteArticleForm()
    if form.validate_on_submit():
        tag_names = re.split(u"[,，]", form.tags.data)
        tag_list = []
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            tag_list.append(tag if tag else Tag(name=tag_name.strip()))
        article = Article(title=form.title.data,
                          content=form.content.data,
                          author_id=current_user.id,
                          category_id=form.category_id.data,
                          tags=tag_list,
                          create_timestramp=datetime.now(),
                          last_edit_timestramp=datetime.now())
        db.session.add(article)
        db.session.commit()
        flash(u"Save Articles successfully!", 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/write_article.html', form=form)


@admin.route('/delete_article/<int:id>')
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)
    if article:
        db.session.delete(article)
        db.session.commit()
        flash(u"Delete artilce %s successfull!" % article.title, 'success')
    else:
        flash(u"Can't find article with id %s" % str(article.id), 'error')
    return redirect(url_for('admin.index'))


@admin.route('/edit_article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    form = WriteArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        article.category_id = form.category_id.data
        tag_names = re.split(u"[,，]", form.tags.data)
        tag_list = []
        for tag_name in tag_names:
            q_tag = Tag.query.filter_by(name=tag_name.strip()).first()
            tag_list.append(q_tag if q_tag else Tag(name=tag_name.strip()))
        article.tags = tag_list
        article.last_edit_timestramp = datetime.now()
        db.session.add(article)
        db.session.commit()
        flash(u"Edit Articles successfully!", 'success')
        return redirect(url_for('main.article', id=article.id))
    form.title.data = article.title
    form.content.data = article.content
    form.category_id.data = article.category_id
    form.tags.data = ','.join([tag.name for tag in article.tags.all()])
    return render_template('admin/write_article.html', form=form)


@admin.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        if Category.query.filter_by(name=form.name.data).first():
            flash(u"Category %s has existed!" % form.name.data, 'error')
            return render_template('admin/add_category.html', form=form)
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(u"Add category successfully!", 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/add_category.html', form=form)


@admin.route('/edit_category', methods=['GET', 'POST'])
@login_required
def edit_category():
    form = EditCategoryForm()
    if form.validate_on_submit():
        category = Category.query.get(form.category_id.data)
        if category:
            category.name = form.new_name.data
            db.session.add(category)
            db.session.commit()
            flash(u"Edit category %s successfull!"
                  % category.name, 'success')
            return redirect(url_for('admin.index'))
        else:
            flash(u"Can't find category with id %s"
                  % str(form.category_id.data), 'error')
    return render_template('admin/edit_category.html', form=form)


@admin.route('/delete_category/', methods=["GET", "POST"])
@login_required
def delete_category():
    form = DeleteCategoryForm()
    if form.validate_on_submit():
        category = Category.query.get(form.category_id.data)
        if category:
            articles = Article.query.filter_by(category_id=category.id)
            for article in articles:
                db.session.delete(article)
            db.session.delete(category)
            db.session.commit()
            flash(u"Delete category %s successfull!"
                  % category.name, 'success')
            return redirect(url_for('admin.index'))
        else:
            flash(u"Can't find category with id %s"
                  % str(form.category_id.data), 'error')
    return render_template('admin/delete_category.html', form=form)


@admin.route('/edit_tag', methods=['GET', 'POST'])
@login_required
def edit_tag():
    form = EditTagForm()
    if form.validate_on_submit():
        old_tag = Tag.query.filter_by(name=form.old_name.data).first()
        if old_tag:
            new_tag = Tag.query.filter_by(name=form.new_name.data).first()
            if new_tag:
                for article in old_tag.articles.all():
                    article.tags = [tag if tag.name != old_tag.name
                                    else new_tag
                                    for tag in article.tags.all()]
                    db.session.add(article)
                    db.session.commit()
            else:
                old_tag.name = form.new_name.data
                db.session.add(old_tag)
                db.session.commit()
            flash(u'Edit tag successfully!', 'success')
            return redirect(url_for('admin.index'))
        else:
            flash(u"Can't find tag with name %s"
                  % str(form.old_tag.data), 'error')
    return render_template('admin/edit_tag.html', form=form)


@admin.route('/delete_tag/', methods=["GET", "POST"])
@login_required
def delete_tag():
    form = DeleteTagForm()
    if form.validate_on_submit():
        tag = Tag.query.filter_by(name=form.tag_name.data).first()
        if tag:
            db.session.delete(tag)
            db.session.commit()
            flash(u"Delete tag %s successfull!"
                  % form.tag_name.name, 'success')
            return redirect(url_for('admin.index'))
        else:
            flash(u"Can't find tag with name %s" % str(form.tag_name.name),
                  'error')
    return render_template('admin/delete_tag.html', form=form)
