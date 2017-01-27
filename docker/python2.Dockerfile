FROM docker.io/mobify/python:2.7.11

WORKDIR /app
COPY requirements.txt .
RUN virtualenv /venv && \
    . /venv/bin/activate && \
    pip install -r requirements.txt && \
    pip install nose
