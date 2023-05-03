from typing_extensions import Annotated

from fastapi import Depends, Header, HTTPException, Security, File, UploadFile
from fastapi.security.api_key import APIKeyHeader

from starlette import status

from sqlalchemy.orm import Session

from users.repository import UserRepository

from core.database import get_db

def get_user_repository(db: Annotated[Session, Depends(get_db)]):
    return UserRepository(db)

def verify_auth_token(authorization: Annotated[APIKeyHeader, Security(APIKeyHeader(name='authorization'))] = None):
    if not authorization:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="User not authenticated")
    return authorization

