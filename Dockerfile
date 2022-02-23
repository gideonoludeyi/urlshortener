FROM python:3.9

WORKDIR /code

RUN pip install poetry

COPY poetry.lock pyproject.toml /code/

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY /urlshortener /code/app/

EXPOSE 8000

CMD [ "poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000" ]

