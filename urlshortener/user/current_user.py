from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError  # type: ignore

from ..client import Client
from ..invalid_credentials import InvalidCredentials
from .jwt import decode_token
from .schema import UserInDB
from .users_db import users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def current_user(token: str = Depends(oauth2_scheme), db: Client = Depends(users_db)) -> UserInDB:
    try:
        payload = decode_token(token)
    except JWTError as e:
        raise InvalidCredentials from e

    user = db.get(key=payload.email)

    if user is None:
        raise InvalidCredentials

    user_in_db = UserInDB(**user)
    if payload.issued_at < user_in_db.ignore_access_tokens_before:
        raise InvalidCredentials

    return user_in_db
