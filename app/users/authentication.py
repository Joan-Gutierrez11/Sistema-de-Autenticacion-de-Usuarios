from fastapi import HTTPException
from starlette import status

from jose import jwt

from security.jwt_handlers import *
from users.repository import UserRepository
from users.models import User

def authenticate_user(username: str, password: str, repository: UserRepository):
    user: User = repository.get_verified_user(username, password)
    if user:        
        token = create_jwt_token_time_grace({ "user_id": user.id })
        return { "token": token, "type": "Bearer" }
    
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail={ "message": "Incorrect credentials" })

def get_user_from_token(token: str, repository: UserRepository):
    try:
        payload = decode_jwt_token(token)
    except jwt.JWTError as jwt_e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=jwt_e.args)
    
    user_id = payload.get('user_id')
    user = repository.get_by_id(user_id)
    return user

def refresh_auth_user_token(token: str, repo: UserRepository):
    try:
        payload = decode_jwt_token_time_grace(token)
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=e.args)

    user_id = payload['user_id']
    if not repo.get_by_id(user_id):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Cannot get token because this user not found")
    
    new_token = create_jwt_token_time_grace({"user_id": user_id })
    return { "token": new_token, "type": "Bearer" }
