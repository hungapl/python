#!/usr/bin/env bash

# Python command
PYTHON=python3
# Docker image tag
IMAGE=python-example

# Build a python wheel distribution
echo 'Building python wheel file ====================='

$PYTHON setup.py bdist_wheel
# Show wheel file
ls dist/*.whl
echo 'Building python wheel file COMPLETED ==========='

# Build docker image
echo 'Building docker image ============================'
docker build . -t $IMAGE # Optionally use -t to add a tag
echo 'Buildling docker image COMPLETED ================='

# Test docker image
echo 'Test docker image by providing two numbers to sum='
PARAM_X=1.0
PARAM_Y=2.0
docker run -t $IMAGE python3 -m my_package.processor $PARAM_X $PARAM_Y
echo 'Test docker image COMPLETED ======================'