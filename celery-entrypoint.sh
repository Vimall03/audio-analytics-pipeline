#!/bin/bash
# Entrypoint for Celery worker

# Wait for DB and Redis to be ready
/wait-for-it.sh postgres:5432 -- echo "Postgres is up"
/wait-for-it.sh redis:6379 -- echo "Redis is up"

# Start Celery worker
exec celery -A app.core.celery_app.celery worker --loglevel=INFO
