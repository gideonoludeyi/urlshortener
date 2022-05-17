import calendar
import os
from datetime import datetime, timedelta

from jose import jwt  # type: ignore
from pydantic import BaseModel

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'a-super-secret-key')
MINUTES_BEFORE_EXPIRY = float(os.getenv('JWT_MINUTES_BEFORE_EXPIRY', '15'))
ALGORITHM = 'HS256'


class Payload(BaseModel):
    email: str
    issued_at: int
    expires_at: int


def serialize_datetime(time: datetime) -> int:
    return calendar.timegm(time.timetuple())


def create_access_token(email: str):
    now = datetime.utcnow()
    data = {
        'sub': email,
        'iat': serialize_datetime(now),
        'exp': serialize_datetime(now + timedelta(minutes=MINUTES_BEFORE_EXPIRY)),
    }
    token: str = jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token: str):
    data: dict = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])

    return Payload(
        email=data['sub'],
        issued_at=data['iat'],
        expires_at=data['exp']
    )
