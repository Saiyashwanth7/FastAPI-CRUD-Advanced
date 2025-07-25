from fastapi import FastAPI
from routers import auth,todos,sample
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(
    bind=engine
)  # This will be executed by the compiler only if the database is not created

app.include_router(auth.router)
app.include_router(todos.router)
#app.include_router(sample.router)