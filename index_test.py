import pytest
from index import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    return app


def test_index(client):
    '''
    Preform test on / endpoint with GET method
        Expect a response code of 200
        Expect the string 'Existing Records' on page
    '''
    with client.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b'Existing Records' in response.data


def test_index_post(client):
    '''
    Preform test on / endpoint with POST method
        Expect a response code of 405, method not allowed
    '''
    with client.test_client() as test_client:
        response = test_client.post('/')
        assert response.status_code == 405


def test_add(client):
    '''
    Preform test on /add endpoint with GET method
        Expect a response code of 200
        Expect the string 'New Food Form' on page
    '''
    with client.test_client() as test_client:
        response = test_client.get('/add')
        assert response.status_code == 200
        assert b'New Food Form' in response.data

def test_add_post(client):
    '''
    Preform test on /add endpoint with POST method
        Expect a response code of 302, redirect
        When trying to add same data again
            Expect status of 200
            Expect string 'already exists' in response data 
    '''
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

def test_delete_item(client):
    '''
    Preform test on /delete route GET method, trying to delete food with id 1, 
    added in above test
        Expect status of 302, redirect
        Expect string 'Food item is deleted' in response data
    '''
    with client.test_client() as test_client:
        response = test_client.get('/delete_food/1')
        assert response.status_code == 302
        response = test_client.get('/add')
        assert b'Food item is deleted' in response.data


def test_delete__post(client):
    '''
    Preform test on /delete POST method, trying to delete food with id 1,
        expect status 405, method not allowed
    Preform test on /delete route POST method, this route does not exists
        expect status 404, not found
    '''
    with client.test_client() as test_client:
        response = test_client.post('/delete_food/1')
        assert response.status_code == 405
        response = test_client.post('/delete')
        assert response.status_code == 404
