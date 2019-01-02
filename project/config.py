
import os
import sys

''' Environment Variable Configuration '''
if os.path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]           

class Config(object):
    SECRET_KEY = "this-really-need-to-be-changed"
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    ERROR_INCLUDE_MESSAGE = False
    RESTPLUS_MASK_SWAGGER = False
    
    ## POSTGRESQL CONFIG
    DB_USER = os.environ.get("PG_USER") or 'root'
    DB_PASSWORD = os.environ.get("PG_PWD") or '!admin'
    DB_NAME = os.environ.get("PG_DBNAME") or 'database'
    DB_HOST = os.environ.get("PG_HOST") or 'localhost'
    DB_PORT = os.environ.get("PG_PORT") or 5432
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_URL") or \
                            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

   
    ## CELERY CONFIG
    REDIS_HOST = os.environ.get("REDIS_HOST") or "localhost"
    REDIS_PORT = os.environ.get("REDIS_PORT") or 6379
    CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

    ## SQLITE
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                         f'sqlite:///{os.path.join(Config.BASEDIR, "data-dev.db")}'
    
    @classmethod
    def init_app(cls, app):
        print ("RUNNING ON DEVELOPMENT MODE")


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    ## SQLITE
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #                         f'sqlite:///{os.path.join(BASEDIR, "data-test.db")}'

    @classmethod
    def init_app(cls, app):
        print ("RUNNING ON TESTING MODE")

class ProductionConfig(Config):
    SECRET_KEY = "Production-Secret-Key-Need-To-Change-Try-To-Create-With-os.urandom"
    SSL_DISABLE = (os.environ.get('SSL_DISABLE') or 'True') == 'True'

    @classmethod
    def init_app(cls, app):
        print ("RUNNING ON PRODUCTION MODE")




config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig
}