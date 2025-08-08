from .utils import *
from ..routers.admin import get_db,decode_token

app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[decode_token] = override_decode_token

def test_read_admin_in_db(create_todo):
    response=client.get("/admin/")
    assert response.status_code == 200
    r=response.json()
    assert len(r) == 1
    
def test_Delete_todo(create_todo):
    response=client.delete("/admin/1")
    assert response.status_code == 204
    db=TestSessionLocal()
    r=db.query(Todo).all()
    assert len(r) == 0