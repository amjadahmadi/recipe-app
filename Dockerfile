FROM python:3.9-alpine3.13
LABEL maintainer="amjadahmadi.de"

ENV PYTHONUNBUFFERED 1
COPY requirements/ /tmp/requirements/
COPY ./requirements.prod.txt /tmp/requirements.prod.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG ENV=prod
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache \
        gcc \
        musl-dev \
        linux-headers \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        postgresql-dev \
        jpeg-dev \
        zlib-dev && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
            build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.${ENV}.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user