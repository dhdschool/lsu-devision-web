#!/bin/bash

set -e

# Run migrations
echo "Running Django migrations..."
python manage.py migrate

# Start Redis server
echo "Starting Redis server..."
redis-server --daemonize yes

# Start Django server
echo "Starting Django server at http://127.0.0.1:8000..."
python manage.py runserver 127.0.0.1:8000 &

# Wait
sleep 2

# Start Celery worker
echo "Starting Celery worker..."
celery -A devision worker --loglevel=info &

echo "All services started."