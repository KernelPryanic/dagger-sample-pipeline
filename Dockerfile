FROM python:3.11-alpine

RUN set -x && \
    addgroup nonroot && \
    adduser -G nonroot -s /bin/sh -D nonroot

USER nonroot
