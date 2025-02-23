from typing import Optional
from pydantic import BaseModel, EmailStr

from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    published:bool =True

class PostCreate(PostBase):
    pass

class user_out(BaseModel):
    id:int
    emails: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:user_out

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    emails: EmailStr
    password:str


class UserLogin(BaseModel):
    emails: EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str

class Token_data(BaseModel):
    id:Optional[str]=None
    