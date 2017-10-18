#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        os.urandom(24)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASK_POST_PER_PAGE = 6
    RECENT_POST = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB') or \
        "sqlite:///" + os.path.join(basedir, "dev_db.sqlite")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import RotatingFileHandler
        rotatingFilelog_handler = RotatingFileHandler(filename='blog_dev.log')
        rotatingFilelog_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(rotatingFilelog_handler)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DB') or \
        "sqlite:///" + os.path.join(basedir, "pro_db.sqlite")


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        import logging
        from logging.handlers import RotatingFileHandler
        rotatingFilelog_handler = RotatingFileHandler(filename='blog.log')
        rotatingFilelog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(rotatingFilelog_handler)


class TestConfig(Config):
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost:7000'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB') or \
        "sqlite:///" + os.path.join(basedir, "test_db.sqlite")


config = {
    "DEFAULT": DevelopmentConfig,
    "DEVELOPMENT": DevelopmentConfig,
    "PRODUCTION": ProductionConfig,
    "TEST": TestConfig,
    "UNIX": UnixConfig
}
