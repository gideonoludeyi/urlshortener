__version__ = '0.1.0'

from string import ascii_letters

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from nanoid import generate


def generate_code():
    valid_chars = f'0123456789{ascii_letters}'
    return generate(alphabet=valid_chars, size=6)

app = FastAPI()

cache = dict()

@app.get('/')
def index():
    return 'Hello world'

@app.post('/', response_class=JSONResponse)
def shorten(url:str):
    code = generate_code()
    while code in cache:
        code = generate_code()
    cache[code] = url
    return dict(code=code)
        

@app.get('/{code}')
def redirect(code:str):
    url = cache.get(code)
    if url is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return RedirectResponse(url)


