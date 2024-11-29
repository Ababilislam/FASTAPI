from typing import List, Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter

from app import oauth2
from .. import models, schemas, utils
from sqlalchemy.orm import Session

from ..database import get_db

router = APIRouter(
    prefix= "/posts", 
    tags = ["Post"]
)
@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), limit:int = 10, skip:int =0, search:Optional[str] = ""):
    # cursor.execute("select * from posts where id=%s", str(id))
    # post = cursor.fetchone()
    # print(limit)
    # print(skip)
    post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("SELECT * FROM posts")
    # posts= cursor.fetchall()
    # posts=db.query(models.Post).all()
    # print(posts)
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post :schemas.PostCreate, db: Session = Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
    # cursor.execute(query="insert into posts (title,content,published) values(%s,%s,%s) returning *", vars=(post.title, post.content, post.published))
    # now_posts= cursor.fetchall()
    # connection.commit()
    # print(**post.dict())
    # print(current_user.id)
    print(current_user.__str__())
    new_posts = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get('/{id}', response_model=schemas.Post)
def get_post(id:int,response: Response,db: Session = Depends(get_db)):
    # cursor.execute("select * from posts where id=%s", str(id))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    # print(post)
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
    # cursor.execute('delete from posts where id=%s returning *', (str(id),))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not exists')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perfom requested action!')
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("update posts set title=%s, content=%s, published=%s where id=%s returning *",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not exists')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perfom requested action!')
    
    post_query.update(updated_post .dict(), synchronize_session=False)

    db.commit()
    return post_query.first()

