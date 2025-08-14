from fastapi import FastAPI,Depends
from .routers import auth,todos,admin,users
from .models import User,Base
from .database import engine,sessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from starlette import status
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(
    bind=engine
)  # This will be executed by the compiler only if the database is not created

app.mount("/static",StaticFiles(directory="ToDoApp/static"),name="static")

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

@app.get("/")
async def home(request:Request):
    return RedirectResponse(url="/todos/todo-page",status_code=status.HTTP_302_FOUND)

@app.get('/health-check')
async def health_chec():
    return {"status":"healthy"}