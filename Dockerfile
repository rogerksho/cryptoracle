#!/bin/bash

# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get -y install gcc && \
    apt-get -y install --reinstall build-essential && \
    apt-get -y install libpq-dev && \
    apt-get -y install git && \
    apt-get autoremove -y && apt-get clean

COPY requirements_pip.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY requirements_aws.txt requirements_aws.txt
RUN pip3 install -r requirements_aws.txt

RUN pip3 install --user --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

COPY . .

CMD ["python3", "-m", "gunicorn", "-b", "0.0.0.0:8000", "app:app"]