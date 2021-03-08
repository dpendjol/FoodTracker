import pytest
from index import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    return app

def test_index(client):
    with client.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200

def test_add(client):
    with client.test_client() as test_client:
        response = test_client.get('/add')
        assert response.status_code == 200

def test_add(client):
    mock_data = {
                 'food-name': 'test2',
                 'protein': 0,
                 'carbohydrates': 0,
                 'fat': 0
                }
    
    with client.test_client() as test_client:
        response = test_client.post('/add', data=(mock_data))
        assert response.status_code == 302
        test_client.post('/add', data=(mock_data))
        response = test_client.get('/add')
        assert response.status_code == 200
        assert b'already exists' in response.data

def test_delete(client):
    with client.test_client() as test_client:
        response = test_client.get('/delete_food/7')
        assert response.status_code == 302