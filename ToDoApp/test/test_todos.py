from .utils import *
from ..routers.todos import get_db, decode_token

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[decode_token] = override_decode_token

def test_read_by_db(create_todo):
    response = client.get("/app/")  # use prefix route of the testing endpoint
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result) == 1
    todo = result[0]
    assert todo["title"] == "Testing"
    assert todo["priority"] == 1
    assert todo["owner"] == 1
    assert (
        todo["description"] == "Need to complete learning unit and integration Testing"
    )
    assert todo["completed"] is False
    assert todo["DueDate"] == "2025-08-06"
    assert todo["id"] == 1


def test_read_one_db(create_todo):
    response = client.get("/app/todo/1")  # use prefix route of the testing endpoint
    assert response.status_code == status.HTTP_200_OK
    result = (
        response.json()
    )  # We can't diresctly compare a json with db output,json must be stored in dict
    assert result.get("title") == "Testing"
    assert result.get("priority") == 1
    assert result.get("owner") == 1
    assert (
        result.get("description")
        == "Need to complete learning unit and integration Testing"
    )
    assert result.get("completed") == False


def test_read_404_db(create_todo):
    response = client.get("/app/todo/123")  # use prefix route 0of the testing endpoint
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo of the id does not exists"}


def test_Create_todo(create_todo):
    request_data = {
        "title": "Test create todo",
        "priority": 1,
        "description": "Testing the create-todo endpoint",
        "completed": False,
        "duedate": "2025-08-10",
    }

    response = client.post("/app/todo/create/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    request_model = db.query(Todo).filter(Todo.title == request_data["title"]).first()
    assert request_model.title == request_data.get("title")
    assert request_model.id == 2


def test_update_todo(create_todo):
    update_data = {
        "title": "Test create todo",
        "priority": 5,
        "description": "Testing the create-todo endpoint",
        "completed": False,
        "duedate": "2025-08-07",
    }
    response = client.put("/app/todo/update/1", json=update_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_todo(create_todo):
    response = client.delete("/app/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model is None
