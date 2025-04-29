# Docker Compose Configuration for Jarvis

This directory contains Docker configuration files for deploying the Jarvis application on a Raspberry Pi 4, connecting to an existing PostgreSQL database running on a Raspberry Pi 3.

## System Architecture

- **Django Backend**: Runs on Raspberry Pi 4
- **Nginx**: Acts as a reverse proxy, runs on Raspberry Pi 4
- **PostgreSQL**: Already configured and running on Raspberry Pi 3 (192.168.1.128)

## Setup Instructions

### Prerequisites

- Raspberry Pi 4 with Docker and Docker Compose installed
- Raspberry Pi 3 with PostgreSQL running in Docker
- Network connectivity between the two Raspberry Pis

### Configuration

1. Copy the example environment file and edit it:
   ```bash
   cp env.example .env
   nano .env
   ```

2. Modify environment variables to match your setup:
   - Set a strong `SECRET_KEY`
   - Update `ALLOWED_HOSTS` if necessary
   - Ensure database connection details match your PostgreSQL setup on RPI3
   - Configure superuser credentials

### Deployment

To start the services:

```bash
cd /path/to/infrastructure
docker-compose up -d
```

To stop the services:

```bash
docker-compose down
```

To view logs:

```bash
docker-compose logs -f
```

## Resource Optimization

The Docker Compose configuration includes resource limits optimized for Raspberry Pi 4:

- Django backend: 512MB memory limit, 0.75 CPU
- Nginx: 128MB memory limit, 0.3 CPU

These limits can be adjusted in the `docker-compose.yml` file based on your specific Raspberry Pi model and requirements.

## Health Checks and Reliability

- Containers are configured with `restart: unless-stopped` policy
- The Django service includes health checks
- The entrypoint script waits for PostgreSQL to be available before starting

## Troubleshooting

If you encounter issues:

1. Check connectivity to PostgreSQL on RPI3:
   ```bash
   ping 192.168.1.128
   ```

2. Verify PostgreSQL is accepting connections:
   ```bash
   nc -zv 192.168.1.128 5432
   ```

3. Check container logs:
   ```bash
   docker-compose logs django
   docker-compose logs nginx
   ``` 