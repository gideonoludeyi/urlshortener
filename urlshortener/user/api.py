import calendar
from curses import raw
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError  # type: ignore

from ..client.base import Client
from ..client.inmemoryclient import InMemoryClient
from .jwt import create_access_token, decode_token
from .pwd import hash_password, verify_password
from .schema import User, UserInDB

router = APIRouter()


client = InMemoryClient()

client.set('johndoe@example.com', {
    "email": "johndoe@example.com",
    "hashed_password": "$2b$12$TtB2fBC0v4K1PfCwteiSD.Pd9Xuopkbl3K2hFll5/rj6wZw3yVzuW",
})

client.set('alice@example.com', {
    "email": "alice@example.com",
    "hashed_password": "$2b$12$1uAZBYM2t7NmBDuS67j.P.lln1SDnTcb5ZTp.yfxkuDBbrJZYuy.y",
})


def get_db():
    return client


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Client = Depends(get_db)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
    except JWTError as e:
        raise credentials_exception from e

    user = db.get(key=payload.email)

    if user is None:
        raise credentials_exception

    user_in_db = UserInDB(**user)
    if payload.issued_at < user_in_db.ignore_access_tokens_before:
        raise credentials_exception

    return user_in_db


@router.get('/')
def current_user(user: UserInDB = Depends(get_current_user)):
    return User(**user.dict())


def authenticate_user(email: str, password: str, db: Client) -> User | None:
    user = db.get(email)
    if user is not None:
        user_in_db = UserInDB(**user)
        if verify_password(password=password, hashed_password=user_in_db.hashed_password):
            return User(**user_in_db.dict())
        else:
            return None
    else:
        return None


@router.post('/token')
def login(form: OAuth2PasswordRequestForm = Depends(), db: Client = Depends(get_db)):
    user = authenticate_user(
        email=form.username,
        password=form.password,
        db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        email=user.email,
        expires_delta=timedelta(minutes=15))
    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/create', status_code=status.HTTP_201_CREATED)
def signup(form: OAuth2PasswordRequestForm = Depends(), db: Client = Depends(get_db)):
    email = form.username
    hashed_password = hash_password(form.password)

    user = UserInDB(email=email, hashed_password=hashed_password)

    if db.exists(user.email):
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail='Email already in use')

    db.set(key=user.email, data=user.dict())


@router.post('/logout')
def logout(user: UserInDB = Depends(get_current_user), db: Client = Depends(get_db)):
    now = datetime.utcnow()
    user.ignore_access_tokens_before = calendar.timegm(now.timetuple())
    db.set(key=user.email, data=user.dict())
