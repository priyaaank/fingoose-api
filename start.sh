#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Starting the application..."
gunicorn --bind 0.0.0.0:8000 wsgi:app 