FROM python:3.9-alpine3.13
LABEL maintainer="vangastructurals.com"

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     rm -rf /tmp ** \
#     adduser \
#         --disabled-password \
#         --no-create-home \
#         django-user

ARG DEV=false
RUN echo "Creating virtual environment" && python -m venv /py \
    && echo "Upgrading pip" && /py/bin/pip install --upgrade pip \
    && echo "Adding dependency packages postresql-client" && apk add --update --no-cache postgresql-client \
    && echo "Adding virtual temp build dependencies together" && apk add --update --no-cache --virtual .tmp-build-deps \
            build-base postgresql-dev musl-dev \
    && echo "Installing requirements" && /py/bin/pip install -r /tmp/requirements.txt \
    && echo "Performing check for development envt installs" && if [ $DEV="true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
        fi \
    && echo "Removing temporary files" && rm -rf /tmp \
    && echo "Removing postresql adapter build dependencies" && apk del .tmp-build-deps \
    && echo "Adding user" && adduser --disabled-password --no-create-home django-user


ENV PATH="/py/bin:$PATH"

USER django-user