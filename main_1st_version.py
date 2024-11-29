from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from  fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool =True
    rating: Optional[int]=None


my_posts= [{'title':'first post 1', 'content':'content of 1st post', 'rating':4, 'id':1},{'title':'first post 2', 'content':'content of 2nd post', 'rating':4.5 , 'id':2}]


def findpost(id):
    for p in my_posts:
        if p['id'] ==id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
        

@app.get('/')
def root():
    return {"message":"hello ab welcome to my api"}


@app.get('/posts')
def get_posts():
    return {"data":my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict=post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post}


@app.get('/posts/{id}')
def get_post(id:int, response: Response):
    post = findpost(id) 
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f' post with id {id} not found'}
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {0} not found'.format(id))
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    print(post)
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {0} not found'.format(id))
    post_dict =post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message":"post updated"}



 
