from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


#################################################
##########         User Schemas        ##########
#################################################
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


#################################################
##########         Post Schemas        ##########
#################################################
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostAndVotesResponse(BaseModel):
    Post: PostResponse
    votes: int


#################################################
##########         Login Schemas       ##########
#################################################
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]


#################################################
##########         Vote Schemas        ##########
#################################################
class Vote(BaseModel):
    post_id: int
    dir: int
