FROM python:3.11.4-slim-bookworm

RUN apt update && \
    apt install -y gpg zip postgresql jq && \
    apt upgrade -y

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY version.json /code/app/version.json

COPY ./tls /tls

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8443", "--ssl-keyfile", "/tls/private.key", "--ssl-certfile", "/tls/certificate.crt"]
