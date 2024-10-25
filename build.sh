#!/bin/bash

# Build the project
set -o errexit  # exit on error
echo "Building the project JDA..."




pip install -r requirements.txt

python manage.py collectstatic --no-input
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
