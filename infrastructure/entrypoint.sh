#!/bin/sh

set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
python -c "
import sys
import time
import psycopg2

host = '${DB_HOST:-192.168.1.128}'
port = '${DB_PORT:-5432}'
dbname = '${DB_NAME:-database}'
user = '${DB_USER:-olivier}'
password = '${DB_PASSWORD}'

for i in range(30):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.close()
        sys.exit(0)
    except psycopg2.OperationalError:
        print(f'Waiting for PostgreSQL {i}/30')
        time.sleep(2)

sys.exit(1)
"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if specified in environment variables
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput || echo "Superuser already exists."
fi

# Execute the command passed to docker CMD
exec "$@" 