from .utils import *
from ..routers.auth import get_db,authenticate_user,create_token,SECRET_KEY,ALGORITHM,decode_token
from datetime import timedelta
from jose import jwt
import pytest_asyncio
from fastapi import HTTPException

app.dependency_overrides[get_db]=override_get_db

def test_authenticate_user(testing_user):
    db=TestSessionLocal()
    authenticated_user=authenticate_user(testing_user.username,"1913101243",db)
    assert authenticated_user is not False
    assert authenticated_user.username == testing_user.username

def test_create_user(testing_user):
    request={
        "email": "EmailStr@gmal.com",
    "username": "username_test",
    "first_name": "first_name",
    "last_name": "last_name",
    "password": "Passw0rd",
    "role": "admin"
    }
    response=client.post("/auth/",json=request)
    assert response.status_code == 201
    p=response.json()
    db=TestSessionLocal()
    r=db.query(User).filter(User.username == "username_test").first()
    assert r.id == 2
    assert p["password"] == "Passw0rd"
    
    
def test_Create_token(testing_user):
    token=create_token(testing_user.username,testing_user.id,testing_user.role,timedelta(minutes=30))
    assert token is not None
    
    decode=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    assert decode["sub"] == testing_user.username
    assert decode["id"] == testing_user.id
    assert decode["role"] == testing_user.role
    
    
@pytest.mark.asyncio
async def test_Decode_token():
    encode={"sub":"username","id":1,"role":"admin"}
    token = jwt.encode(encode,SECRET_KEY,ALGORITHM)
    decode = await decode_token(token)
    assert decode["sub"] == "username"
    assert decode["id"] == 1
    assert decode["role"] == "admin"
    
@pytest.mark.asyncio
async def test_Decode_token_401():
    encode={"role":"admin"}
    token = jwt.encode(encode,SECRET_KEY,ALGORITHM)
    
    with pytest.raises(HTTPException) as expconf:   
        await decode_token(token)
        
    assert expconf.value.status_code == 401
    assert expconf.value.detail == "Unauthorized user"