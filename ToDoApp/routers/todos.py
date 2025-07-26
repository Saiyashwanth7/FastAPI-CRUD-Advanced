from fastapi import FastAPI, Depends, Path, HTTPException,APIRouter
from typing import Annotated
import models
from models import Todo
from database import engine, sessionLocal
from sqlalchemy.orm import session
from starlette import status
from pydantic import BaseModel, Field
from .auth import decode_token

router = APIRouter(
    prefix='/app',
    tags=['todos']
)

class TodoRequest(BaseModel):
    title: Annotated[str, Field(min_length=7)]
    description: Annotated[str, Field(min_length=15)]
    priority: Annotated[int, Field(ge=1, le=5)]
    completed: Annotated[bool, Field(default=False)]


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# the above function will deal with accessing to the DB , we will be using this
# function everywhere so here we are closing the db with db.close


"""now we need a Dependency injection which will get the return from the get_db function for which we use Depends()
from the fastapi"""

db_dependency = Annotated[session, Depends(get_db)]

user_dependency = Annotated[dict,Depends(decode_token)]


# we can either use the above variable or directly the Annotated[....] in the below endpoint
@router.get("/")
async def read_db(db: db_dependency):
    return db.query(Todo).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo of the id does not exists")


@router.post("/todo/create", status_code=status.HTTP_201_CREATED)
async def create_todo(newtodo: TodoRequest, db: db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "Authenication failed")
    
    todo_record = Todo(
        title=newtodo.title,
        description=newtodo.description,
        priority=newtodo.priority,
        completed=newtodo.completed,
        owner=user.get('id')
    )
    """
        instead of above code we can also use below one:
        todo_record=Todo(**newtodo.model_dump())
    """
    db.add(todo_record)
    db.commit()


@router.put("/todo/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, update_todo: TodoRequest, todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo_model:
        raise HTTPException(status_code=404, detail="Invalid ID")

    todo_model.title = update_todo.title
    todo_model.description = update_todo.description
    todo_model.priority = update_todo.priority
    todo_model.completed = update_todo.completed

    db.add(todo_model)
    db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tod(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="the id doesnot exists")

    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
