from datetime import datetime, timedelta
from jose import jwt  # type: ignore
from pydantic import BaseModel
import calendar


class Payload(BaseModel):
    email: str
    issued_at: int
    expires_at: int


def create_access_token(email: str, expires_delta: timedelta = timedelta(minutes=15)):
    now = datetime.utcnow()
    data = {
        'sub': email,
        'iat': calendar.timegm(now.timetuple()),
        'exp': calendar.timegm((now + expires_delta).timetuple()),
    }
    token: str = jwt.encode(data, key='SECRET_KEY', algorithm='HS256')
    return token


def decode_token(token: str):
    json_data = token.split(' ', maxsplit=1)[1]  # strip off 'Bearer ' header

    data: dict = jwt.decode(
        json_data, key='SECRET_KEY', algorithms=['HS256'])

    return Payload(
        email=data['sub'],
        issued_at=data['iat'],
        expires_at=data['exp']
    )
