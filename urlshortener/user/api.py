from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

from ..client.base import Client
from .current_user import current_user
from .jwt import create_access_token, serialize_datetime
from .pwd import hash_password, verify_password
from .schema import User, UserInDB
from .users_db import users_db

router = APIRouter(tags=['user'])


def authenticate_user(email: str, password: str, db: Client) -> User | None:
    user = db.get(email)
    if user is not None:
        user_in_db = UserInDB(**user)
        if verify_password(password, user_in_db.hashed_password):
            return User(**user_in_db.dict())
        else:
            return None
    else:
        return None


@router.get('/', response_model=User)
def show_current_user(user: UserInDB = Depends(current_user)):
    return dict(user)


class Token(BaseModel):
    access_token: str = Field(
        title='The JWT access token for clients to perform authenticated requests')
    token_type: str = Field(title='The type of token (bearer, basic, e.t.c)')


@router.post('/token', response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Client = Depends(users_db)):
    user = authenticate_user(
        email=form.username,
        password=form.password,
        db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(email=user.email)
    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(form: OAuth2PasswordRequestForm = Depends(), db: Client = Depends(users_db)):
    email = form.username
    hashed_password = hash_password(form.password)

    user = UserInDB(email=email, hashed_password=hashed_password)

    if db.exists(user.email):
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail='Email already in use')

    db.set(key=user.email, data=dict(user))


@router.post('/logout')
def logout(user: UserInDB = Depends(current_user), db: Client = Depends(users_db)):
    now = datetime.utcnow()
    user.ignore_access_tokens_before = serialize_datetime(now)
    db.set(key=user.email, data=dict(user))
