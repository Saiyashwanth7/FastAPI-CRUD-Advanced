from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..routers.todos import get_db, decode_token
from ..models import Base
from ..main import app
from fastapi.testclient import TestClient
from starlette import status
import pytest
from ..models import Todo
from datetime import date, datetime, timezone


# in this we will create a mock database which we only use for testing.SQLIte would work just fine.
# We will create the test.db similar to the todos.db sqlite but add poolclass to create a single connection request
SQL_ALCHEMY_DB = "sqlite:///./test.db"

engine = create_engine(
    SQL_ALCHEMY_DB, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)

# In todos.py , we use get_db and decode_token functions as dependencies for db_dependency and user_dependency respectively
"""while testing we need to connect to the mock database we created instead of the production database 
so we override the get_db function and add the TestingSessionLocal().
Also in the user_dependency we will authenticate the user, but here in case of testing we use mock users ,can't 
be authenticated, so we override the decode_token function to make it return a dict of mock user
"""


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_decode_token():
    return {"username": "testuser", "id": 1, "role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[decode_token] = override_decode_token

client = TestClient(app)


@pytest.fixture
def create_todo():
    new_todo = Todo(
        title="Testing",
        description="Need to complete learning unit and integration Testing",
        priority=1,
        completed=False,
        owner=1,
    )
    db = TestingSessionLocal()
    db.add(new_todo)
    db.commit()
    yield new_todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todolist"))
        connection.commit()


def test_read_by_db(create_todo):
    response = client.get("/app/")  # use prefix route of the testing endpoint
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "Testing",
            "priority": 1,
            "owner": 1,
            "description": "Need to complete learning unit and integration Testing",
            "id": 1,
            "completed": False,
        }
    ]

def test_read_one_db(create_todo):
    response = client.get("/app/todo/1")  # use prefix route of the testing endpoint
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
            "title": "Testing",
            "priority": 1,
            "owner": 1,
            "description": "Need to complete learning unit and integration Testing",
            "id": 1,
            "completed": False,
        }

def test_read_404_db(create_todo):
    response = client.get("/app/todo/123")  # use prefix route 0of the testing endpoint
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail":"Todo of the id does not exists"}
"""def test_create_todo(create_todo):
    pass"""