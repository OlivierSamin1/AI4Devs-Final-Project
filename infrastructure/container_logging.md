# Container Logging Configuration

This document describes the logging configuration for Docker containers in the Jarvis application.

## Overview

All Docker containers in the Jarvis application are configured to use the `json-file` logging driver with rotation enabled to prevent disk space issues on the Raspberry Pi.

## Log Configuration Details

### Logging Driver
- **Driver**: json-file (Docker's default)
- **Max Size**: 10MB per log file
- **Max Files**: 3 (rotation will keep 3 files before deleting old logs)
- **Compression**: Enabled to save disk space
- **Tags**: Each log entry is tagged with the service name and container ID

### Access to Logs

To view logs for each container, use the following Docker commands:

```bash
# View logs for Django application
docker compose logs django

# View logs for Nginx
docker compose logs nginx

# Follow logs in real-time
docker compose logs -f [service_name]

# View logs with timestamps
docker compose logs -t [service_name]

# View limited number of lines
docker compose logs --tail=100 [service_name]
```

### Log Storage

Log files are stored in the Docker daemon's data directory, typically:
- Linux: `/var/lib/docker/containers/<container-id>/<container-id>-json.log`
- The exact location may vary based on your Docker configuration

## Best Practices for Application Logging

1. **Log to stdout/stderr**: Application code should log to stdout/stderr rather than to files
2. **Structured logging**: Use JSON-formatted logs when possible
3. **Include context**: Add request IDs, user info, and relevant metadata
4. **Log levels**: Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
5. **Security**: Never log sensitive data (passwords, tokens, personal information)

## Performance Considerations for Raspberry Pi

The logging configuration has been optimized for Raspberry Pi:
- Log rotation prevents excessive disk usage
- Compression reduces storage requirements
- Max file size and count are set to conserve resources
- Log tags help with quick identification without complex parsing

## Troubleshooting

If logs are not being captured properly:
1. Verify the Docker daemon is running
2. Check that the application is writing to stdout/stderr
3. Ensure there is sufficient disk space available
4. Restart the Docker daemon if log rotation is not working as expected

## Security Considerations

- Access to logs should be restricted to authorized personnel
- Logs may contain sensitive information and should be protected accordingly
- Regular log reviews should be conducted for security monitoring 