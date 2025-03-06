import os
from dotenv import load_dotenv
import pymysql

# Install PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost/personal_finance'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for API
    JSON_SORT_KEYS = False
    # Disable redirects for trailing slashes
    APPLICATION_ROOT = '/api'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value) 