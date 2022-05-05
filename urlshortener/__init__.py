import os
from string import ascii_letters, digits

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from nanoid import generate

from .client import Client
from .clouddsclient import CloudDatastoreClient

SERVICE_ACCOUNT_FILEPATH = os.getenv('SERVICE_ACCOUNT_FILEPATH')


def generate_code():
    valid_chars = f'{digits}{ascii_letters}'
    return generate(alphabet=valid_chars, size=6)


client: Client = CloudDatastoreClient(
    kind='urls',
    service_account_filename=SERVICE_ACCOUNT_FILEPATH)

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
    return RedirectResponse(url=url)
