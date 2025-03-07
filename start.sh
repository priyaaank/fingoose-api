#!/bin/bash
set -e

# Set up MySQL character set
mysql -h mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SET NAMES utf8mb4; SET CHARACTER SET utf8mb4;"

echo "Running database migrations..."
flask db upgrade

echo "Starting the application..."
gunicorn --bind 0.0.0.0:5000 wsgi:app 