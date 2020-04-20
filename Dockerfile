FROM python:3.6-slim

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD . /src
COPY ./src src 

WORKDIR /src

CMD gunicorn --bind 0.0.0.0:5000 src.wsgi:app
