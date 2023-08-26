FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
ENV APP_NAME=aciniformes_backend
ENV APP_MODULE=${APP_NAME}.routes.base:app

COPY ./requirements.txt /app/
COPY ./logging_prod.conf /app/
COPY ./logging_test.conf /app/
RUN pip install --no-cache-dir -U -r /app/requirements.txt

COPY ./alembic.ini /alembic.ini
COPY ./migrations /migrations/

RUN echo '#!/bin/bash \n\
\n\
alembic upgrade head' > /app/prestart.sh \
    && chmod +x /app/prestart.sh

COPY . /app
