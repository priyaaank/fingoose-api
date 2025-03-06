# Use Python 3.9 slim image
FROM python:3.9-slim

# Set environment variables
ENV FLASK_APP=wsgi.py

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Initialize migrations directory if it doesn't exist
RUN flask db init || true

# Expose port
EXPOSE 5000

# Run migrations and start application
CMD flask db upgrade && gunicorn --bind 0.0.0.0:5000 wsgi:app 