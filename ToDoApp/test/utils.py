from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..models import Base, Todo, User
from fastapi.testclient import TestClient
from ..main import app
import pytest
from starlette import status
from datetime import date
from ..routers.todos import get_db, decode_token
from ..routers.auth import bcrypt_context

SQL_ALCHEMY_URL = "sqlite:///./test.db"

engine = create_engine(SQL_ALCHEMY_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)


# Dependency overrides
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_decode_token():
    return {"sub": "sai_yashwanth_Dasari", "id": 1, "role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[decode_token] = override_decode_token

client = TestClient(app)


# Fixture for test todo
@pytest.fixture
def create_todo():
    db = TestSessionLocal()
    todo = Todo(
        title="Testing rn",
        description="Description for the test",
        priority=5,
        completed=False,
        DueDate=date(2025, 8, 12),
        owner=1,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)

    yield todo
    # Clean up DB
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todolist;"))
        connection.commit()
    db.close()


@pytest.fixture
def testing_user():
    new_user = User(
        email="dasarisaiyashwanth@gmail.com",
        username="sai_yashwanth_Dasari",
        first_name="Sai Yashwanth",
        last_name="Dasari",
        hashed_password=bcrypt_context.hash("1913101243"),
        role="admin",
    )
    db = TestSessionLocal()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    yield new_user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM usertable;"))
        connection.commit()
    db.close()
