from string import ascii_letters, digits

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from nanoid import generate  # type: ignore

from .client import Client
from .client.inmemoryclient import InMemoryClient
from .user.api import router as user_router


def generate_code():
    valid_chars = f'{digits}{ascii_letters}'
    return generate(alphabet=valid_chars, size=6)


def get_client():
    with InMemoryClient() as client:
        yield client


app = FastAPI()

app.include_router(user_router, prefix='/user')

templates = Jinja2Templates(directory='templates')


@app.get('/')
def root(request: Request):
    return templates.TemplateResponse('index.html.jinja2', {'request': request})


@app.post('/', response_class=JSONResponse)
def shorten(request: Request, url: str = Form(...), client: Client = Depends(get_client)):
    code = generate_code()
    while client.exists(code):
        code = generate_code()

    client.set(code, {'url': url})
    return templates.TemplateResponse('url.html.jinja2', {'request': request, 'code': code})


@app.get('/login')
def login(request: Request):
    return templates.TemplateResponse('login.html.jinja2', {'request': request})


@app.get('/r/{code}')
def redirect(code: str, client: Client = Depends(get_client)):
    data = client.get(code)
    if data is None:
        raise HTTPException(status_code=404, detail="Code not found")

    url = data['url']
    return RedirectResponse(url=url)
