#!/bin/bash

openssl req -newkey rsa:2048 -nodes -keyout private.key -x509 -days 365 -addext "subjectAltName = DNS:localhost" -out certificate.crt