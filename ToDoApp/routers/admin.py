from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status
from .auth import decode_token
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import sessionLocal
from ..models import Todo

router=APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict,Depends(decode_token)]


# we can either use the above db_dependency variable or directly the Annotated[....] in the below endpoint
@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_db(db: db_dependency,user:user_dependency):
    if not user or user.get("role")!='admin':
        raise HTTPException(status_code=401,detail='Invalid')
    return db.query(Todo).all()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(...,ge=1)):
    if not user or user.get("role")!='admin':
        raise HTTPException(status_code=401,detail='Invalid')
    todo_model=db.query(Todo).filter(Todo.id==todo_id).first()
    db.delete(todo_model)
    db.commit()
    