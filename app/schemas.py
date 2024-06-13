
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
# from pydantic.types import conint   // deprecated
from typing_extensions import Annotated
from pydantic import BaseModel, Field
 

# //declear user register validation here
class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str 


class UserResponse(BaseModel):
    id:int
    name: str
    email: EmailStr
    is_active: bool
    created_at:datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class Login(BaseModel):
    email:EmailStr
    password:str    


# //declear post validation here
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  
    # owner_id:int


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    owner_id:int
    created_at:datetime
    owner:UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id:Optional[int] = None
    # sub:EmailStr


class Vote(BaseModel):
    post_id:int
    dir: Annotated[int, Field(strict=True, le=1)] #value must be an integer and be 0 and 1

    

