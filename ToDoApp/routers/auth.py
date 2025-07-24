from fastapi import APIRouter,Depends
from pydantic import BaseModel,EmailStr,Field
from typing import Annotated,Optional
from database import sessionLocal,engine
from sqlalchemy.orm import session
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta,datetime,timezone
from jose import jwt

class UserRequest(BaseModel):
    email: EmailStr
    username: Annotated[str,Field(min_length=3)]
    first_name: Annotated[Optional[str],Field(min_length=1)]
    last_name: Annotated[Optional[str],Field(min_length=1)]
    password: Annotated[str,Field(min_length=8)]
    role: str
    
    
class Token(BaseModel):
    access_token : str
    token_type:str
    
    
router = APIRouter()

SECRET_KEY="d5bbc198a5de8cb2e71245d6ee97a9d993f199689a5c0922a1803170274f5be0"
ALGORITHM="HS256"
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session, Depends(get_db)]

def authenticate_user(username:str,password:str,db):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_token(username:str,user_id:int,expires_delta:timedelta):
    encode={
        "sd":username,
        "id":user_id
    }
    expires=datetime.now(timezone.utc) + expires_delta
    encode.update({"exp":expires})
    
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

@router.post("/auth")
async def create_user(db:db_dependency,userrequest:UserRequest):
    new_user=User(
        email=userrequest.email,
        username=userrequest.username,
        first_name=userrequest.first_name,
        last_name=userrequest.last_name,
        hashed_password=bcrypt_context.hash(userrequest.password),
        role=userrequest.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    
    return new_user

@router.post('/token',response_model=Token)
async def login_for_access_token(form:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=authenticate_user(form.username,form.password,db)
    if  not user:
        return "Falied Authentication"
    token=create_token(user.username,user.id,timedelta(minutes=30))
    return {'access_token':token,'token_type':'bearer'}