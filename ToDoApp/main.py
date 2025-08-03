from fastapi import FastAPI,Depends
from .routers import auth,todos,admin,users
from .models import User,Base
from .database import engine,sessionLocal
from sqlalchemy.orm import Session
from typing import Annotated

app = FastAPI()

Base.metadata.create_all(
    bind=engine
)  # This will be executed by the compiler only if the database is not created

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

@app.get('/health-check')
async def health_chec():
    return {"status":"healthy"}