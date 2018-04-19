import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.api.scraping import get_news_links, download_articles,process_articles

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    JOBS = [
        {
            'id': None,
            'func': get_news_links,
            'trigger': 'interval',
            'minutes': 30,
            'replace_existing': True
        },
        {
            'id': None,
            'func': download_articles,
            'trigger': 'interval',
            'minutes': 1,
            'replace_existing': True
        },
        {
           'id': None,
           'func': process_articles,
           'trigger': 'interval',
           'minutes': 5,
           'replace_existing': True
        }
    ]

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///flask_context.db')
    }

    SCHEDULER_API_ENABLED = False



class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'APP_PRODUCTION_DATABASE_URI'
    # )
    SQLALCHEMY_DATABASE_URI = 'postgres://keynews:123456@postgres:5432/keynews'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'APP_DEVELOPMENT_DATABASE_URI'
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'APP_TESTING_DATABASE_URI'
    )


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': ProductionConfig,
}
