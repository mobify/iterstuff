FROM docker.io/mobify/python:3.5

WORKDIR /app
COPY requirements.txt .
RUN pyvenv /venv && \
    . /venv/bin/activate && \
    pip install wheel nose && \
    pip install -r requirements.txt
