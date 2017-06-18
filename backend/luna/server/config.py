# geoguide/server/config.py

import os
from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = config('APP_KEY')
    DEBUG = config('DEBUG', False, cast=bool)
    BCRYPT_LOG_ROUNDS = config('BCRYPT_LOG_ROUNDS', 13, cast=int)
    DEBUG_TB_ENABLED = config('DEBUG_TB_ENABLED', False, cast=bool)
    DEBUG_TB_INTERCEPT_REDIRECTS = config('DEBUG_TB_INTERCEPT_REDIRECTS', False, cast=bool)


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = config('DEBUG', True, cast=bool)
    BCRYPT_LOG_ROUNDS = config('BCRYPT_LOG_ROUNDS', 4, cast=int)
    DATABASE_URL = config(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    DATABASE_URL = 'sqlite:///'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = config('DEBUG', False)
    DATABASE_URL = config(
        'DATABASE_URL', 'postgresql://localhost/example')
