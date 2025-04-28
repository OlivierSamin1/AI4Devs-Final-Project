# Backend Container Restart Troubleshooting

## Issue Description
The Docker container for the backend service is experiencing an endless restart loop with the following error:
```
[2025-04-21 15:15:39 +0000] [1] [ERROR] Worker (pid:7) exited with code 1
```

This error indicates that a Gunicorn worker process is exiting with a non-zero exit code, causing the container to restart due to the `restart: always` directive in the docker-compose.yml.

## Potential Causes and Investigation Steps

### 1. Database Connection Issues
- **Check if PostgreSQL is accessible:**
  ```bash
  docker-compose exec backend python -c "import psycopg2; conn = psycopg2.connect(dbname='database', user='olivier', password='tazmanland80', host='192.168.1.128', port='5432')"
  ```
- **Verify connection details** in settings.py match the actual database configuration
- **Ensure the PostgreSQL server** at 192.168.1.128 is running and accepts connections

### 2. Redis Connection Issues
- **Check if Redis is accessible:**
  ```bash
  docker-compose exec backend python -c "import redis; r = redis.Redis.from_url('redis://redis:6379/1'); r.ping()"
  ```
- **Verify the Redis service** is running and properly configured in the Docker network

### 3. Application Code Errors
- **Check Django logs** by modifying docker-compose.yml to capture container output:
  ```yaml
  backend:
    # Existing configuration...
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
  ```
- **Enable verbose error reporting** in settings.py by ensuring DEBUG is set to True

### 4. Environment Variables
- **Verify .env file exists** and contains all required variables
- **Check for syntax errors** in the .env file

### 5. Filesystem Issues
- **Check for permission problems** on mounted volumes
- **Ensure sufficient disk space** is available

### 6. Resource Constraints
- **Monitor CPU and memory usage** to ensure the container has adequate resources
- **Check for OOM (Out of Memory) kills** in Docker or system logs

### 7. Gunicorn Configuration
- **Review Gunicorn settings** in the Dockerfile
- **Try modifying Gunicorn parameters** to troubleshoot:
  ```
  CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "--log-level", "debug", "jarvis.wsgi:application"]
  ```

## Immediate Debugging Steps

1. **View detailed container logs:**
   ```bash
   docker logs $(docker ps -q -f name=backend) 2>&1
   ```

2. **Start the container in interactive mode for debugging:**
   ```bash
   docker-compose run --rm backend bash
   # Then inside the container:
   python manage.py check
   python manage.py runserver 0.0.0.0:8000
   ```

3. **Check Gunicorn directly:**
   ```bash
   docker-compose run --rm backend gunicorn --bind 0.0.0.0:8000 --log-level debug jarvis.wsgi:application
   ```

4. **Check for module import issues:**
   ```bash
   docker-compose run --rm backend python -c "import django; print(django.__version__)"
   ```

## Long-term Solutions

1. **Implement better logging** for application and infrastructure monitoring
2. **Add health checks** to the Docker configuration
3. **Set up monitoring tools** like Prometheus and Grafana
4. **Create container restart policies** with appropriate delays and retry limits
5. **Implement graceful failure handling** in the application code

Please review these suggestions and let me know which direction you'd like to pursue first. 