# geoguide/server/config.py

import os
from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = config('APP_KEY')
    DEBUG = config('DEBUG', False, cast=bool)
    BCRYPT_LOG_ROUNDS = config('BCRYPT_LOG_ROUNDS', 13, cast=int)
    SQLALCHEMY_TRACK_MODIFICATIONS = config(
        'SQLALCHEMY_TRACK_MODIFICATIONS', False, cast=bool)


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = config('DEBUG', True, cast=bool)
    BCRYPT_LOG_ROUNDS = config('BCRYPT_LOG_ROUNDS', 4, cast=int)
    SQLALCHEMY_DATABASE_URI = config(
        'SQLALCHEMY_DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = config('DEBUG', False)
    SQLALCHEMY_DATABASE_URI = config(
        'SQLALCHEMY_DATABASE_URI', 'postgresql://localhost/example')
