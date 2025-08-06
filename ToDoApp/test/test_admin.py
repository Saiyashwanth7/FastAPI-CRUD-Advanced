from .utils import *
from ..routers.admin import get_db,decode_token

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[decode_token] = override_decode_token

def test_read_db_admin(create_todo):
    # The fixture creates a todo, now test the admin endpoint
    response = client.get("/admin/") 
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result) == 1
    todo = result[0]
    assert todo["title"] == "Testing"
    
def test_delete_id(create_todo):
    response=client.delete("/admin/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    result = db.query(Todo).filter(Todo.id == 1).first()
    assert result is None
    
def test_delete_404_id(create_todo):
    response=client.delete("/admin/1234")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    

def test_not_admin(create_todo):
    response = client.get("/admin/")
    assert response.status_code == status.HTTP_403_FORBIDDEN