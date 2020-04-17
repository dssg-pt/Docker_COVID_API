FROM python:3.6-slim
ADD . /src
WORKDIR /src
RUN pip install --no-cache-dir -r requirements.txt
CMD python ./src/flask_server.py