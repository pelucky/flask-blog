#!/usr/bin/env python
# -*- coding=utf-8 -*-

from flask import (render_template, request,
                   current_app, flash, redirect, url_for)
from ..models import User
from . import main
from ..models import Article, Category, Tag
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(
        Article.create_timestramp.desc()).paginate(
            page,
            per_page=current_app.config['FLASK_POST_PER_PAGE'],
            error_out=False)
    one_page_articles = pagination.items
    articles = Article.query.order_by(Article.create_timestramp.desc())
    categories = Category.query
    tags = Tag.query
    return render_template('index.html', articles=articles,
                           categories=categories,
                           tags=tags,
                           one_page_articles=one_page_articles,
                           pagination=pagination)


@main.route('/about_me')
def about_me():
    user = User.query.filter_by(id=1).first()
    return render_template('about_me.html', user=user)


@main.route('/aritcle/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    Article.add_one_view(article)
    return render_template('article.html', article=article)


@main.route('/archive')
def archive():
    articles = Article.query.order_by(Article.create_timestramp.desc())
    categories = Category.query
    tags = Tag.query
    return render_template('archive.html', articles=articles,
                           categories=categories, tags=tags)


@main.route('/category/<string:name>')
def category(name):
    articles = Article.query.order_by(Article.create_timestramp.desc())
    categories = Category.query
    tags = Tag.query
    category = Category.query.filter_by(name=name).first_or_404()
    return render_template('category.html', category=category,
                           articles=articles, categories=categories,
                           tags=tags)


@main.route('/tag/<string:name>')
def tag(name):
    articles = Article.query.order_by(Article.create_timestramp.desc())
    tags = Tag.query
    categories = Category.query
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag, categories=categories,
                           articles=articles, tags=tags)


@main.route('/search')
def search():
    keywords = request.args.get('query', type=unicode)
    if keywords:
        articles = Article.query.order_by(Article.create_timestramp.desc())
        categories = Category.query
        page = request.args.get('page', 1, type=int)
        pagination = Article.query.order_by(
            Article.create_timestramp.desc()).filter(
            Article.title.like('%' + keywords + '%')).paginate(
            page,
            per_page=current_app.config['FLASK_POST_PER_PAGE'],
            error_out=False)
        query_articles = pagination.items
        return render_template('search.html', articles=articles,
                               categories=categories,
                               query_articles=query_articles,
                               keywords=keywords,
                               pagination=pagination)
    flash("You should search something!", "warning")
    return redirect(url_for('main.index'))


def make_external(url):
    return urljoin(request.url_root, url)


@main.route('/rss')
def rss():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    articles = Article.query.order_by(Article.create_timestramp.desc()) \
                      .limit(15).all()
    for article in articles:
        feed.add(article.title, unicode(article.markdown_html),
                 content_type='html',
                 author=User.query.get(article.author_id).nickname,
                 url=make_external(url_for('main.article', id=article.id)),
                 updated=article.last_edit_timestramp)
    return feed.get_response()
