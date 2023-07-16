FROM python:3
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
ENV APP_NAME=pinger_backend
ENV APP_MODULE=${APP_NAME}.service.scheduler:ApSchedulerService().start()

COPY ./requirements.txt /app/
COPY ./logging_prod.conf /app/
COPY ./logging_test.conf /app/

RUN pip install -U -r /app/requirements.txt

COPY ./${APP_NAME} /app/${APP_NAME}
