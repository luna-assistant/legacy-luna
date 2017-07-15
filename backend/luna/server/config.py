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
    DB_HOST = config('DB_HOST', '127.0.0.1')
    DB_PORT = config('DB_PORT', 5432, cast=int)
    DB_DATABASE = config('DB_DATABASE', 'postgres')
    DB_USERNAME = config('DB_USERNAME', 'postgres')
    DB_PASSWORD = config('DB_PASSWORD', 'postgres')
    BROKER_URL = 'iot.eclipse.org'
    BROKER_PORT = 443
    BROKER_SSL = True


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = config('DEBUG', True, cast=bool)
    BCRYPT_LOG_ROUNDS = config('BCRYPT_LOG_ROUNDS', 4, cast=int)    


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = config('DEBUG', False)
