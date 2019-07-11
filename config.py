"""Configure the app based on which environment it's running in."""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Define the base class for configurations."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@metro.scope'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'password'
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or None
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or None

    @staticmethod
    def init_app(app):
        """Define the base class init method."""
        pass


class DevelopmentConfig(Config):
    """Extend the base class for development."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    """Extend the base class for testing."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    """Extend the base class for production."""

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
