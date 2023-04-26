import datetime

from pydantic import BaseModel, create_model

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

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class IncorrectPassword(BaseModel):
    message: str



