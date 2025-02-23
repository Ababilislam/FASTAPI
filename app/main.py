from fastapi import FastAPI
from app import models
from .database import engine
from .routers import post, user, auth
from . import config


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {"message":"hello ab welcome to my api"}
