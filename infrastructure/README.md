# Docker Compose Configuration for Jarvis

This directory contains Docker configuration files for deploying the Jarvis application on a Raspberry Pi 4, connecting to an existing PostgreSQL database running on a Raspberry Pi 3.

## System Architecture

- **Django Backend**: Runs on Raspberry Pi 4 (ARM64)
- **Nginx**: Acts as a reverse proxy, runs on Raspberry Pi 4
- **PostgreSQL**: Already configured and running on Raspberry Pi 3 (192.168.1.128)

## Setup Instructions

### Prerequisites

- Raspberry Pi 4 with Docker and Docker Compose installed
- Raspberry Pi 3 with PostgreSQL running in Docker (already set up)
- Network connectivity between the two Raspberry Pis

### Configuration

1. Create an environment file:
   ```bash
   # Example .env file
   # Django settings
   DEBUG=True
   SECRET_KEY=your_secure_key
   ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.10
   
   # Database settings - Connect to existing PostgreSQL on RPI3
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=database
   DB_USER=olivier
   DB_PASSWORD=your_password
   DB_HOST=192.168.1.128
   DB_PORT=5432
   
   # Superuser credentials
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=secure_password
   ```

2. Make sure the PostgreSQL on RPI3 is configured to accept connections:
   - PostgreSQL should be listening on all interfaces 
   - pg_hba.conf should allow connections from your network

### Deployment

To start the services:

```bash
cd /path/to/infrastructure
docker compose up -d
```

To stop the services:

```bash
docker compose down
```

To view logs:

```bash
docker compose logs -f
```

## Architecture Details

### Django Container
- Uses ARM64-compatible Python 3.10 image
- Runs with host network mode to directly access PostgreSQL on RPI3
- Automatically waits for PostgreSQL to be available
- Applies database migrations on startup
- Creates a superuser if specified
- Handles static files collection
- Uses Gunicorn as the application server

### Nginx Container
- Lightweight ARM64-compatible Alpine-based image
- Acts as a reverse proxy to Django
- Serves static and media files
- Exposed on port 8080 (http://your-rpi4-ip:8080)

## Resource Optimization

- CPU resource limits to prevent overloading the Raspberry Pi
- Non-root users for both containers
- Alpine-based Nginx for minimal footprint
- Error resilience with automatic restart policies

## Accessing the Application

Once deployed, the application can be accessed at:
- Web interface: http://your-rpi4-ip:8080
- Django admin: http://your-rpi4-ip:8080/admin/

## Troubleshooting

If you encounter issues:

1. Check container status:
   ```bash
   docker ps
   ```

2. Check container logs:
   ```bash
   docker logs infrastructure-django-1
   docker logs infrastructure-nginx-1
   ```

3. Verify PostgreSQL connectivity:
   ```bash
   nc -zv 192.168.1.128 5432
   ```

4. Check if environment variables are properly set in .env file

5. For permission issues with static files, make sure DEBUG=True in your .env file during development 