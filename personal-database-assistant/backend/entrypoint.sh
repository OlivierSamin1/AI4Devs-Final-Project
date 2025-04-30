#!/bin/sh

set -e

# PostgreSQL connection settings
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_WAIT_TIMEOUT=${DB_WAIT_TIMEOUT:-30}

# Function to check if PostgreSQL is available
postgres_ready() {
    python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${DB_NAME:-health_db}",
        user="${DB_USER:-postgres}",
        password="${DB_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(1)
sys.exit(0)
END
}

# Wait for PostgreSQL if needed
echo "Waiting for PostgreSQL..."
if [ -n "$DB_HOST" ] && [ "$DB_HOST" != "localhost" ] && [ "$DB_HOST" != "127.0.0.1" ]; then
    # External database - wait for it
    i=0
    while [ $i -lt $DB_WAIT_TIMEOUT ]; do
        if postgres_ready; then
            break
        fi
        i=$((i+1))
        echo "Waiting for PostgreSQL $i/$DB_WAIT_TIMEOUT"
        sleep 1
    done
    
    if [ $i -eq $DB_WAIT_TIMEOUT ]; then
        echo "PostgreSQL is unavailable - continuing without it (some features may not work)"
    fi
else
    echo "Using local/mock database - skipping PostgreSQL check"
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput || echo "Migration failed, but continuing..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static files collection failed, but continuing..."

# Create superuser if specified
echo "Creating superuser..."
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput || echo "Superuser already exists."
else
    echo "Superuser environment variables not set."
fi

# Start Gunicorn
exec "$@" 