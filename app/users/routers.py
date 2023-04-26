from typing import List, Dict, Any, Union
from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader

from fastapi_pagination import Page, Params

import users.schemas as user_schemas
import users.models as user_models

from users.dependencies import *
from users.repository import UserRepository
from users.authentication import *


auth_router = APIRouter(
    prefix='/auth'
)

@auth_router.post('/login')
def login(login_form: user_schemas.LoginRequest, 
        repo: Annotated[UserRepository, Depends(get_user_repository)]):
    """
    URL path to perform user login

    Args:
        login_form (user_schemas.LoginRequest): Pydantic scheme that verifies sending 
            username and password
        
        repo (Annotated[UserRepository, Depends): User Repository that is responsible 
            for verifying the correct credentials of a user

    Returns:
        Dict[str, str]: A Json data that contains the authorization token and the token type
    """

    return authenticate_user(repository=repo, **login_form.dict())

@auth_router.get('/user', 
            response_model=user_schemas.User)
def get_user_authenticated(repo: Annotated[UserRepository, Depends(get_user_repository)],
        authorization = Security(APIKeyHeader(name='Authorization'))):
    """
    URL path to get a User information by auth token.

    Args:
        repo (Annotated[UserRepository, Depends): User Repository that is responsible 
            for verifying the correct credentials of a user

        authorization (str, None): Authorization Token that allow user access to this path.
            Defaults to Security(APIKeyHeader(name='Authorization')).

    Returns:
        user_schemas.User: schema that contains all information of user
    """

    return get_user_from_token(authorization, repository=repo)

@auth_router.get('/refresh')
def refresh_auth_token(authorization: Annotated[str, Depends(verify_auth_token)]):
    return refresh_auth_jwt_token(authorization)



# @auth_router.post('/logout')
# def logout():
#     ...

# 
# User Info Endpoints
# 

user_router = APIRouter(
    prefix='/user',
)

@user_router.get('/{id}', response_model=user_schemas.User)
def get_user(id: int, repo: Annotated[UserRepository, Depends(get_user_repository)]):
    """
    """

    return repo.get_by_id(id)

@user_router.get('', response_model=List[user_schemas.User])
def get_all_users(repo: Annotated[UserRepository, Depends(get_user_repository)]):
    """
    """

    return repo.all()

@user_router.get('/paginate', response_model=Page[user_schemas.User])
def get_users_by_page(repo: Annotated[UserRepository, Depends(get_user_repository)], 
                params: Params = Depends()):
    """
    """

    return repo.paginate_all_users(params)

@user_router.post('/', response_model=user_schemas.User)
def add_user(new_user: user_schemas.UserInsert, 
        repo: Annotated[UserRepository, Depends(get_user_repository)]):
    """
    """
    user = user_models.User(**new_user.dict())
    user.set_password(new_user.password)
    return repo.create(user)

@user_router.put('/{id}', response_model=user_schemas.User)
def update_user(id: int, 
            user_update: user_schemas.UserUpdate, 
            repo: Annotated[UserRepository, Depends(get_user_repository)]):    
    """
    """
    user = user_update.dict()
    return repo.update(user, id)

@user_router.put('/{id}/change-password', 
            response_model= user_schemas.User,
            responses={ 403: { 'model':user_schemas.IncorrectPassword } })
def change_password_user(id: int, 
                    passwords: user_schemas.UserChangePassword, 
                    repo: Annotated[UserRepository, Depends(get_user_repository)]):
    """
    """

    user: user_models.User = repo.get_by_id(id)
    if not user.verify_password(passwords.old_password):
        return JSONResponse(status_code=403, content={"message": "Incorrect User Password"})

    return repo.update_user_password_by_id(id, passwords.new_password)


@user_router.delete('/{id}', response_model=user_schemas.User)
def delete_user(id:int, repo: Annotated[UserRepository, Depends(get_user_repository)]):
    """
    """

    return repo.delete(id)
