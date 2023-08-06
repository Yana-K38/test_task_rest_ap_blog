FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql-client

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app

CMD  ["gunicorn", "blog_api.wsgi:application", "--bind", "0:8000" ] 
