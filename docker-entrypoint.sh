#!/bin/sh

# Keeps Python from generating .pyc files in the container
export PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
export PYTHONUNBUFFERED=1

source /usr/local/docker-registry-mrproper/.venv/bin/activate
exec /usr/local/docker-registry-mrproper/docker_registry_mrproper.py
