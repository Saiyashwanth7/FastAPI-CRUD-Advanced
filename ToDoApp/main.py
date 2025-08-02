from fastapi import FastAPI,Depends
from routers import auth,todos,admin,users
import models
from models import User
from database import engine,sessionLocal
from sqlalchemy.orm import Session
from typing import Annotated

app = FastAPI()

models.Base.metadata.create_all(
    bind=engine
)  # This will be executed by the compiler only if the database is not created

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency=Annotated[Session,Depends(get_db)]

@app.get('/read-users-db')
async def read_user_db(db:db_dependency):
    return db.query(User).all()
    