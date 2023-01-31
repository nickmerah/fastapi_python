from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BasePost):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(BasePost):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostResponseVote(BasePost):
    votes: int
    Post: PostResponse

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
