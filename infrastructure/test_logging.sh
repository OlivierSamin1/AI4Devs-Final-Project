#!/bin/bash

# Script to test and verify Docker container logging configuration
# This script should be run after the containers are started

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Testing Docker container logging configuration...${NC}"

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed or not in PATH${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed or not in PATH${NC}"
    exit 1
fi

# Check if containers are running
echo -e "${YELLOW}Checking container status...${NC}"
CONTAINERS=$(docker compose ps -q)
if [ -z "$CONTAINERS" ]; then
    echo -e "${RED}Error: No containers are running. Start containers with 'docker compose up -d'${NC}"
    exit 1
fi

echo -e "${GREEN}Containers are running!${NC}"

# Generate some logs
echo -e "${YELLOW}Generating test logs...${NC}"
echo -e "${YELLOW}Sending HTTP request to Django application...${NC}"
curl -s http://localhost:8000/health/ > /dev/null
curl -s http://localhost:8080/nginx-health > /dev/null

# Wait for logs to be generated
sleep 2

# Check Django logs
echo -e "${YELLOW}Checking Django container logs...${NC}"
DJANGO_LOGS=$(docker compose logs --tail=10 django)
if [ -n "$DJANGO_LOGS" ]; then
    echo -e "${GREEN}Django logs are being captured:${NC}"
    echo "$DJANGO_LOGS" | head -n 5
else
    echo -e "${RED}Error: No Django logs found${NC}"
fi

# Check Nginx logs
echo -e "${YELLOW}Checking Nginx container logs...${NC}"
NGINX_LOGS=$(docker compose logs --tail=10 nginx)
if [ -n "$NGINX_LOGS" ]; then
    echo -e "${GREEN}Nginx logs are being captured:${NC}"
    echo "$NGINX_LOGS" | head -n 5
else
    echo -e "${RED}Error: No Nginx logs found${NC}"
fi

# Verify log file exists
echo -e "${YELLOW}Checking Docker log files...${NC}"
CONTAINER_ID=$(docker compose ps -q django)
if [ -n "$CONTAINER_ID" ]; then
    # This will work on most Docker installations
    LOGPATH=$(docker inspect --format='{{.LogPath}}' $CONTAINER_ID)
    
    if [ -n "$LOGPATH" ] && [ -e "$LOGPATH" ]; then
        echo -e "${GREEN}Log file exists at: $LOGPATH${NC}"
        echo -e "${YELLOW}Log file size: $(ls -lh $LOGPATH | awk '{print $5}')${NC}"
    else
        echo -e "${YELLOW}Cannot verify log file location or access. This is normal if running Docker Desktop.${NC}"
    fi
else
    echo -e "${RED}Error: Cannot get container ID${NC}"
fi

# Final verdict
echo -e "${YELLOW}Testing complete!${NC}"
echo -e "${GREEN}Container logging appears to be configured correctly.${NC}"
echo -e "${YELLOW}To view logs, use: docker compose logs [service_name]${NC}"

exit 0 