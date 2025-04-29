# Docker Containers Documentation

## Container Health Checks
Implemented health checks for Docker containers to ensure that unhealthy containers can be automatically restarted.

### Access Commands
- **Django Health Check**:
  ```bash
  curl -f http://localhost:8000/health/
  ```

- **Nginx Health Check**:
  ```bash
  curl -f http://localhost/nginx-health
  ```

## Container Logging
Implemented structured logging for Docker containers using the `json-file` logging driver. This includes:
- Log rotation to manage disk space effectively.
- JSON formatted logs for better readability and analysis.
- Integration with the Django application for capturing logs directly from stdout/stderr.

### Access Commands
- **View Django Logs**:
  ```bash
  docker compose logs django
  ```

- **View Nginx Logs**:
  ```bash
  docker compose logs nginx
  ```

- **Follow Logs in Real-Time**:
  ```bash
  docker compose logs -f [service_name]
  ```

- **View Logs with Timestamps**:
  ```bash
  docker compose logs -t [service_name]
  ```

- **View Limited Number of Lines**:
  ```bash
  docker compose logs --tail=100 [service_name]
  ```