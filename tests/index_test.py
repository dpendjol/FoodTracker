import pytest
from index import create_app
from models import *

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
        

def test_create_log(client):
    with client.test_client() as test_client:
        mock_data = {
                     'date': '2020-02-02'
                     }
        response = test_client.get('/create_log', data=mock_data)
        assert response.status_code == 405
        response = test_client.post('/create_log', data=mock_data)
        assert response.status_code == 302
        response = test_client.get('/')
        assert b'log for date 2020-02-02 created'

def test_add_food_to_log(client):
    food, created = Food.get_or_create(name="Beenham", protein=10, carbs=10, fats=10)
    assert food.name == "Beenham"
    assert food.protein == 10
    assert food.carbs == 10
    assert food.fats == 10
    
    mock_data = {
        'food-select': 1
    }
    
    with client.test_client() as test_client:
        response = test_client.get('/add_food_to_log')
        assert response.status_code == 405
        response = test_client.post('/add_food_to_log/1', data=mock_data)
        assert response.status_code == 500

