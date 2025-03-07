import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URL') or \
    'mysql://test_user:test_password@localhost/personal_finance_test?charset=utf8mb4' 