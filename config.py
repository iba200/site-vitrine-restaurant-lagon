import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-prod'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16MB max upload
    ITEMS_PER_PAGE = 25
    # Business defaults
    CAPACITY = int(os.environ.get('CAPACITY') or 50)
    # Reservation / business defaults
    DEFAULT_TABLE_DURATION_MINUTES = int(os.environ.get('DEFAULT_TABLE_DURATION_MINUTES') or 120)
    RESERVATION_MIN_HOURS = int(os.environ.get('RESERVATION_MIN_HOURS') or 2)
    RESERVATION_MAX_DAYS = int(os.environ.get('RESERVATION_MAX_DAYS') or 60)
    # Opening hours as a JSON-like structure (dict): keys are weekdays (0=Monday)
    DEFAULT_OPENING_HOURS = {
        '0': None, # Monday closed
        '1': {'lunch': ['12:00', '14:30'], 'dinner': ['19:00', '22:30']},
        '2': {'lunch': ['12:00', '14:30'], 'dinner': ['19:00', '22:30']},
        '3': {'lunch': ['12:00', '14:30'], 'dinner': ['19:00', '22:30']},
        '4': {'lunch': ['12:00', '14:30'], 'dinner': ['19:00', '22:30']},
        '5': {'lunch': ['12:00', '14:30'], 'dinner': ['19:00', '22:30']},
        '6': {'lunch': ['12:00', '14:30'], 'dinner': ['19:00', '22:30']},
    }
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite') # Default to sqlite if not provided, but mostly PG in prod

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
