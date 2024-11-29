from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from passlib.context import CryptContext
from  fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine,get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# row sql driver connection.

while True:
    try:
        connection = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='12', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Connection established")
        break
    except Exception as e:
        print( 'connection  to the database failed \n "error" : ' + str(e) )
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {"message":"hello ab welcome to my api"}




 
