from typing import List, Dict, Any, Union
from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Security, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader

from fastapi_pagination import Page, Params

from core.dependencies import get_filesystem, LocalFileSystem

import users.schemas as user_schemas
import users.models as user_models

from users.dependencies import *
from users.repository import UserRepository
from users.authentication import *


auth_router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@auth_router.post('/signup', response_model=user_schemas.User)
def register_user(new_user: user_schemas.UserInsert, repo: Annotated[UserRepository, Depends(get_user_repository)]):
    user = user_models.User(**new_user.dict())
    user.set_password(new_user.password)
    return repo.create(user)

@auth_router.post('/login')
def login(login_form: user_schemas.LoginRequest, repo: Annotated[UserRepository, Depends(get_user_repository)]):
    return authenticate_user(repository=repo, **login_form.dict())

@auth_router.get('/user', response_model=user_schemas.User)
def get_user_authenticated(repo: Annotated[UserRepository, Depends(get_user_repository)], 
        authorization = Security(APIKeyHeader(name='Authorization'))):
    user = get_user_from_token(authorization, repository=repo)
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="User not found")
    return user

@auth_router.get('/refresh')
def refresh_auth_token(authorization: Annotated[str, Depends(verify_auth_token)],
                repo: Annotated[UserRepository, Depends(get_user_repository)]):
    return refresh_auth_user_token(authorization, repo)



# 
# User Info Endpoints
# 

user_router = APIRouter(
    prefix='/user',
    tags=['User Information']
)

@user_router.put('/update', response_model=user_schemas.User)
def update_user(repo: Annotated[UserRepository, Depends(get_user_repository)],
            authorization: Annotated[str, Depends(verify_auth_token)], storage: Annotated[LocalFileSystem, Depends(get_filesystem)], 
            form: Annotated[user_schemas.UserToUpdate, Depends(user_schemas.UserToUpdate)]):    
    user = get_user_from_token(authorization, repo)
    data_to_update = form.dict()

    if form.profile_image:
        new_filename = f'{user.id}-{form.username or user.username}'
        path = storage.upload_file('images/users/profile-pictures', new_filename, form.profile_image)
        data_to_update['profile_image'] = path

    return repo.update(data_to_update, user.id)

@user_router.delete('/delete', response_model=user_schemas.User)
def delete_user(repo: Annotated[UserRepository, Depends(get_user_repository)], authorization: Annotated[str, Depends(verify_auth_token)]):
    user = get_user_from_token(authorization, repo)
    return repo.delete(user.id)

@user_router.put('/change-password', 
            response_model= user_schemas.User,
            responses={ 403: { 'model':user_schemas.IncorrectPassword } })
def change_password_user(authorization: Annotated[str, Depends(verify_auth_token)], passwords: user_schemas.UserChangePassword, 
            repo: Annotated[UserRepository, Depends(get_user_repository)]):
    user: user_models.User = get_user_from_token(authorization, repo)
    if not user.verify_password(passwords.old_password):
        return JSONResponse(status_code=403, content={"message": "Incorrect User Password"})

    return repo.update_user_password_by_id(user.id, passwords.new_password)
