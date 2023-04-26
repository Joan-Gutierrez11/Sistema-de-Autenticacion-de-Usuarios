from fastapi import HTTPException
from starlette import status

from jose import jwt

from security.jwt_handlers import *
from users.repository import UserRepository
from users.models import User

def authenticate_user(username: str, password: str, repository: UserRepository):
    user: User = repository.get_verified_user(username, password)
    if user:        
        return { "token": create_access_token({ "user_id": user.id }), "type": "Bearer" }
    
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail={ "message": "Incorrect credentials" })


def check_token(token: str):
    try:
        return jwt.decode(token, SECRET)
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={ 'message': e.args })

def get_user_from_token(token: str, repository: UserRepository):    
    payload = check_token(token)
    user_id = payload.get('user_id')
    user = repository.get_by_id(user_id)
    return user


def refresh_auth_jwt_token(token: str):
    new_token = refresh_token(token, ['user_id'])
    return { "token": new_token, "type": "Bearer" }
