# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /mini-inventory

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV RUNNING_IN_DOCKER=true

CMD ["flask", "run"]

