from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from .auth import decode_token
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from database import sessionLocal
from models import Todo, User
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field


class UserRequest(BaseModel):
    email: EmailStr
    username: Annotated[str, Field(min_length=3)]
    first_name: Annotated[Optional[str], Field(min_length=1)]
    last_name: Annotated[Optional[str], Field(min_length=1)]
    password: Annotated[str, Field(min_length=8)]
    role: str


router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(decode_token)]

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


class PasswordRequest(BaseModel):
    current_password:str
    new_password:Annotated[str,Field(min_length=8)]

@router.get("/get-user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User"
        )
    user_username = user.get("sub")
    user_id = user.get("id")
    if not user_id or not user_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User"
        )
    user_model = (
        db.query(User)
        .filter(User.id == user_id)
        .filter(User.username == user_username)
        .first()
    )
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found"
        )
    return {
        "email": user_model.email,
        "username": user_model.username,
        "first_name": user_model.first_name,
        "last_name": user_model.last_name,
        "role": user_model.role,
        "hashed_password":user_model.hashed_password,
    }

@router.put('/update-password/')
async def update_password(user:user_dependency,db:db_dependency,passwordrequest:PasswordRequest):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User"
        )
    user_model=db.query(User).filter(User.id==user.get("id")).filter(User.username==user.get("sub")).first()
    if not bcrypt_context.verify(passwordrequest.current_password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='Current password is not valid')
    user_model.hashed_password=bcrypt_context.hash(passwordrequest.new_password)
    db.add(user_model)
    db.commit()
    
#The below method will work but the path parameter would reveal the new password so its better to use the above method
"""@router.put('/change-password/{new_password}',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency,db:db_dependency,new_password:str=Path(...,min_length=8)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User"
        )
        
    user_model=db.query(User).filter(User.id==user.get("id")).filter(User.username==user.get("sub")).first()
    if bcrypt_context.verify(new_password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='New password is same as Old password')
    
    user_model.hashed_password=bcrypt_context.hash(new_password)
    db.add(user_model)
    db.commit()
    
    """
    