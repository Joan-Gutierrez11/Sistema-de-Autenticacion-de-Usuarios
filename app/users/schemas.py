import datetime
from dataclasses import dataclass, asdict
from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, create_model, validator
from pydantic.dataclasses import dataclass as p_dataclass

from fastapi import Form, UploadFile, File

from core.dependencies import get_filesystem

class UserJWT(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    date_joined: datetime.datetime
    profile_image: str

    @validator('profile_image')
    def get_url_image(cls, value):
        if value:
            return get_filesystem().get_url(value)
        return value

    class Config:
        orm_mode = True

class UserInsert(BaseModel):
    username: str
    email: str
    password: str
    first_name: str = None
    last_name: str = None

class UserUpdate(BaseModel):
    id: int = None
    username: str = None
    email: str = None
    first_name: str = None
    last_name: str = None

@dataclass
class UserToUpdate:
    """
    User schema to update data
    """
    username: Annotated[str, Form()] = None 
    first_name: Annotated[str, Form()] = None 
    last_name: Annotated[str, Form()] = None 
    profile_image: Annotated[UploadFile, File()] = None

    def dict(self):
        return asdict(self)

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class IncorrectPassword(BaseModel):
    message: str



