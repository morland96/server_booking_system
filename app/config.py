import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'laksjdlkfdjlkjfdlkjlkasdj'
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=10)
    DEBUG = True
    time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
