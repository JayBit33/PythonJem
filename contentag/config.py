import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////contentag.db'
    # SECRET_KEY = os.environ["SOME_SECRET_KEY"]


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///contentag.db'
    SECRET_KEY = '117038691411f8e2e073e0f04dd0d9d075bea9d8f0b3a240'
