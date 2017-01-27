#!/usr/bin/env bash
echo "Building Python2 image"
docker build --rm -t iterstuff:python2 -f docker/python2.Dockerfile .

echo "Building Python3 image"
docker build --rm -t iterstuff:python3 -f docker/python3.Dockerfile .

echo "Running Python2 tests"
docker run -t --rm \
    -v $(pwd):/app \
    iterstuff:python2 \
    /venv/bin/nosetests /app/iterstuff/tests.py

echo "Running Python3 tests"
docker run -t --rm \
    -v $(pwd):/app \
    iterstuff:python3 \
    /venv/bin/nosetests /app/iterstuff/tests.py
