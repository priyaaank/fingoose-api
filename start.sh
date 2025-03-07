#!/bin/bash
set -e

# Wait for MySQL to be ready
echo "Waiting for MySQL..."
while ! nc -z mysql 3306; do
  sleep 1
done

# Set up MySQL character set
mysql -h mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SET NAMES utf8mb4; SET CHARACTER SET utf8mb4;"

echo "Running database migrations..."
flask db upgrade

echo "Starting the application..."
gunicorn --bind 0.0.0.0:5000 wsgi:app 