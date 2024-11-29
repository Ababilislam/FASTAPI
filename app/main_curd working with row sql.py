
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from  fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

while True:
    try:
        connection = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='12', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Connection established")
        break
    except Exception as e:
        print( 'connection  to the database failed \n "error" : ' + str(e) )
        time.sleep(2)


class Post(BaseModel):
    title:str
    content:str
    published:bool =True
    rating: Optional[int]=None


@app.get('/')
def root():
    return {"message":"hello ab welcome to my api"}


@app.get('/posts')
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts= cursor.fetchall()
    # print(posts)
    return {"data":posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute(query="insert into posts (title,content,published) values(%s,%s,%s) returning *", vars=(post.title, post.content, post.published))
    now_posts= cursor.fetchall()
    connection.commit()
    return {"data":now_posts}


@app.get('/posts/{id}')
def get_post(id:int, response: Response):
    cursor.execute("select * from posts where id=%s", str(id))
    post = cursor.fetchone()
    # print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f' post with id {id} not found'}
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute('delete from posts where id=%s returning *', (str(id),))
    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("update posts set title=%s, content=%s, published=%s where id=%s returning *",(post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    connection.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not exists')
    return {"message":updated_post}



 
