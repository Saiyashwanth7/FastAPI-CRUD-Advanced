from .utils import *
from ..models import User
from ..routers.users import get_db,db_dependency

app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[decode_token] = override_decode_token

def test_get_user(testing_user):
    response=client.get("/user/")
    assert response.status_code == 200
    r=response.json()
    assert r["email"] =="dasarisaiyashwanth@gmail.com"
    assert r["username"] =="sai_yashwanth_Dasari"
    assert r["first_name"] =="Sai Yashwanth"
    assert r["last_name"] =="Dasari"

def test_update_password(testing_user):
    request={
        "current_password":"1913101243",
        "new_password":"123456789"}
    response=client.put("/user/",json=request)
    assert response.status_code == 204