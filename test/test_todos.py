from routers.todos import get_db, get_current_user
from .utils import *
from main import app


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get('/')
    assert response.status_code== status.HTTP_200_OK
    assert response.json() == [{'complete':False, 'title':'todo Title', 'description': 'some description', 'id':1,'priority':5, 'owner_id':1}]

def test_read_one_authenticated(test_todo):
    response = client.get('/todo/1')
    assert response.status_code== status.HTTP_200_OK
    assert response.json() == {'complete':False, 'title':'todo Title', 'description': 'some description', 'id':1,'priority':5, 'owner_id':1}

def test_read_authentication_not_found():
    response = client.get('/todo/11')
    assert response.status_code == 404
    assert response.json() == {'detail':'item not not found'}

def test_create_todo(test_todo):
    request_data={
        'title':'New todo',
        'description': 'some description',
        'priority': 5,
        'complete': False
    }
    response = client.post('/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(2 == Todos.id).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todo):
    request_data = {
        'title': 'Updated title',
        'description': 'some new description',
        'priority': 4,
        'complete': True
    }
    response = client.put('/todo/1', json=request_data)
    assert  response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(1 == Todos.id).first()
    assert model.title == 'Updated title'


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Updated title',
        'description': 'some new description',
        'priority': 4,
        'complete': True
    }
    response = client.put('/todo/99', json=request_data)
    assert  response.status_code == 404
    assert response.json() == {'detail': 'item not not found'}

def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(1 == Todos.id).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/99')
    assert response.status_code == 404
    assert response.json() == {'detail': 'item not not found'}