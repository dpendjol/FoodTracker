import pytest
from index import create_app

@pytest.fixture
def client():
    flask_app = create_app()
    return flask_app

def test_index(client):
    with client.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200

def test_add(client):
    with client.test_client() as test_client:
        response = test_client.get('/add')
        assert response.status_code == 200

def test_add(client):
    with client.test_client() as test_client:
        test_client.post('/add', data=dict(name='test2',
                                           proteins=0,
                                           carbs=0,
                                           fats=0))
        response = test_client.get('/add')
        print(response.data)
        assert 2 == 2