FROM amsterdam/python:3.8-buster
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y
RUN pip install --upgrade pip
RUN pip install uwsgi

WORKDIR /app

COPY /requirements.txt /app/
COPY uwsgi.ini /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY test.sh /app/
COPY .flake8 /app/

COPY belastingen /app/belastingen
COPY entrypoint.sh /app/entrypoint.sh
RUN "mkdir /files && chown datapunt:datapunt /files"

USER datapunt
CMD /bin/sh /app/entrypoint.sh
