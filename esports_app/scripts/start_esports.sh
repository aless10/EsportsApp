#!/bin/bash

# Import the environment vars
export $(egrep -v '^#' .env | xargs)

cd "${PYTHONPATH}"

python /app/esports/manage.py makemigrations
python /app/esports/manage.py migrate
python /app/esports/manage.py createsuperuser --no-input
python /app/esports/manage.py collectstatic --no-input
python /app/esports/manage.py consume_messages

DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE}" gunicorn esports.wsgi:application --bind 0.0.0.0:8000