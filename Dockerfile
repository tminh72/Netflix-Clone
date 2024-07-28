FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN set -e; \
    apt-get update ;\
    apt-get -y install netcat-traditional ;\
    apt-get -y install gettext ;

RUN mkdir /app
COPY . /app/
WORKDIR /app

RUN set -e; \
    /usr/local/bin/python -m pip install --upgrade pip ;\
    python -m pip install -r /app/requirements.txt ;

