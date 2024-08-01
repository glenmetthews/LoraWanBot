FROM python:3.11 AS base

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry

WORKDIR app/

COPY poetry.lock pyproject.toml ./

COPY . .

FROM base AS prod

RUN poetry install --no-interaction --no-ansi --no-dev

RUN alembic upgrade head

