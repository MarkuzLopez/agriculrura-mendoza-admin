
from fastapi import FastAPI
from models import models
from database import engine
from routes import clients, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(clients.router)