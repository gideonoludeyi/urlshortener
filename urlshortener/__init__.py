__version__ = '0.1.0'

import os
from string import ascii_letters

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from nanoid import generate
from redis import Redis


class RedisClient:
    def __init__(self, host: str, port: int, password: str) -> None:
        self.redis = Redis(host=host, port=port, password=password)

    def get(self, code: str) -> str | None:
        return self.redis.get(code)

    def set(self, code: str, url: str) -> None:
        self.redis.set(code, url)

    def exists(self, code: str) -> bool:
        return self.redis.exists(code) == 1


load_dotenv()
REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


def generate_code():
    valid_chars = f'0123456789{ascii_letters}'
    return generate(alphabet=valid_chars, size=6)


client = RedisClient(host=REDIS_HOSTNAME, port=REDIS_PORT,
                     password=REDIS_PASSWORD)
app = FastAPI()


@app.get('/')
def root():
    return 'Hello world'


@app.post('/', response_class=JSONResponse)
def shorten(url: str):
    code = generate_code()
    while client.exists(code):
        code = generate_code()
    client.set(code, url)
    return dict(code=code)


@app.get('/{code}')
def redirect(code: str):
    url = client.get(code)
    if url is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return RedirectResponse(url=url.decode('utf-8'))
