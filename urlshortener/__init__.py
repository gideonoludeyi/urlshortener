import os
from string import ascii_letters, digits

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from nanoid import generate

from .client import Client, get_cloud_datastore_client


def generate_code():
    valid_chars = f'{digits}{ascii_letters}'
    return generate(alphabet=valid_chars, size=6)


def get_client():
    SERVICE_ACCOUNT_FILEPATH = os.getenv('SERVICE_ACCOUNT_FILEPATH')
    return get_cloud_datastore_client(service_account_filepath=SERVICE_ACCOUNT_FILEPATH)


app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get('/')
def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/', response_class=JSONResponse)
def shorten(url: str = Form(...), client: Client = Depends(get_client)):
    code = generate_code()
    while client.exists(code):
        code = generate_code()
    client.set(code, url)
    return dict(code=code)


@app.get('/{code}')
def redirect(code: str, client: Client = Depends(get_client)):
    url = client.get(code)
    if url is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return RedirectResponse(url=url)
