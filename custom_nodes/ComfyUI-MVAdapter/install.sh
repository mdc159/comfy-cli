#!/bin/bash

# Ensure we're using Python 3.11
poetry env use python3.11

# Install dependencies
poetry install

# Download required models
poetry run python download_models.py 