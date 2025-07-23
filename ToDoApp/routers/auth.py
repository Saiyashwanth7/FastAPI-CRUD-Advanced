from fastapi import APIRouter,Depends
from pydantic import BaseModel,EmailStr,Field
from typing import Annotated,Optional
from database import sessionLocal,engine
from sqlalchemy.orm import session
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

class UserRequest(BaseModel):
    email: EmailStr
    username: Annotated[str,Field(min_length=3)]
    first_name: Annotated[Optional[str],Field(min_length=1)]
    last_name: Annotated[Optional[str],Field(min_length=1)]
    password: Annotated[str,Field(min_length=8)]
    role: str

router = APIRouter()

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
    return True


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

@router.post('/token')
async def user_authentication(form:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=authenticate_user(form.username,form.password,db)
    if user:
        return "Successful Authentication"
    return "Failed Authenication"