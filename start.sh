#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Starting the application..."
gunicorn --bind 0.0.0.0:5000 wsgi:app 