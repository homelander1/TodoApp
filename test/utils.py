
from fastapi.testclient import TestClient # force to run as test
from fastapi import status
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker

import main
from database import Base
import pytest
from models import Todos, Users
from routers.auth import brecypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False}, poolclass=StaticPool)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'a1', 'id':1, 'user_role':'admin'}



client = TestClient(main.app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = 'todo Title',
        description = 'some description',
        priority = 5,
        complete = False,
        owner_id = 1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()



@pytest.fixture
def test_user():
    user = Users(
        username="a1",
        email="asdfd@email.com",
        first_name="asdf",
        last_name="asdf",
        hashed_password=brecypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

