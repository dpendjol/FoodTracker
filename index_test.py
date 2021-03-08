import pytest
from index import create_app


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


def test_add_post(client):
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
        assert b'Food already exists' in response.data

# test dependant on test_add_post
def test_delete_food(client):
    with client.test_client() as test_client:
        response = test_client.get('/delete_food/1')
        assert response.status_code == 302
        response = test_client.get('/')
        assert b'Food item is deleted' in response.data
