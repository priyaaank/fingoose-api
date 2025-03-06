import pytest
from app import create_app
from app.database import db
import json
import os

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URL') or 'mysql://test_user:test_password@localhost/personal_finance_test'
    
    with app.app_context():
        db.create_all()
        
    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_goal(client):
    response = client.post('/api/goals/', json={
        'type': 'Retirement',
        'name': 'Retirement 2050',
        'target_amount': 1000000.0,
        'current_value': 100000.0,
        'target_date': '2050-12',
        'expected_inflation': 3.0
    })
    
    assert response.status_code == 201
    assert 'id' in response.json
    
def test_get_goals(client):
    # First create a goal
    client.post('/api/goals/', json={
        'type': 'Education',
        'name': 'College Fund',
        'target_amount': 500000.0,
        'current_value': 50000.0,
        'target_date': '2030-08',
        'expected_inflation': 5.0
    })
    
    response = client.get('/api/goals/')
    assert response.status_code == 200
    assert len(response.json) > 0 