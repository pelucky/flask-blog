import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        os.urandom(24)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_POST_PER_PAGE = 6
    RECENT_POST = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB') or \
        "sqlite:///" + os.path.join(basedir, "dev_db.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DB') or \
        "sqlite:///" + os.path.join(basedir, "pro_db.sqlite")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB') or \
        "sqlite:///" + os.path.join(basedir, "test_db.sqlite")


config = {
    "DEFAULT": DevelopmentConfig,
    "DEVELOPMENT": DevelopmentConfig,
    "PRODUCTION": ProductionConfig,
    "TEST": TestConfig,
}
