from string import ascii_letters, digits

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from nanoid import generate  # type: ignore
from pydantic import BaseModel, Field, HttpUrl

from .client import Client
from .client.inmemoryclient import InMemoryClient
from .user.api import router as user_router
from .user.current_user import current_user

load_dotenv()


def generate_code():
    valid_chars = f'{digits}{ascii_letters}'
    return generate(alphabet=valid_chars, size=6)


def get_client():
    with InMemoryClient() as client:
        yield client


app = FastAPI()

app.mount('/static', app=StaticFiles(directory='web/build/static'), name='static')

app.include_router(user_router, prefix='/user')


@app.get('/', response_class=FileResponse)
def index():
    return FileResponse('web/build/index.html')


class ShortenData(BaseModel):
    url: HttpUrl = Field(title="The url to shorten")


@app.post('/url', response_class=JSONResponse, dependencies=[Depends(current_user)])
def shorten(request: Request, body: ShortenData, client: Client = Depends(get_client)):
    code = generate_code()
    while client.exists(code):
        code = generate_code()

    client.set(code, {'url': body.url})

    return {
        'url': f'{request.base_url}r/{code}'
    }


@app.get('/r/{code}', response_class=RedirectResponse)
def redirect(code: str, client: Client = Depends(get_client)):
    data = client.get(code)
    if data is None:
        raise HTTPException(status_code=404, detail="Code not found")

    return data['url']
