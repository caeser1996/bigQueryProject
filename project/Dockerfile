FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN apk add gcc python3-dev linux-headers build-base
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/