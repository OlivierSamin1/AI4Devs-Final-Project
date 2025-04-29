#!/bin/bash

# Script to test Docker container health checks
# This script will test each health check feature systematically

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Environment variables
DJANGO_CONTAINER="infrastructure-django-1"
NGINX_CONTAINER="infrastructure-nginx-1"
COMPOSE_FILE="infrastructure/docker-compose.yml"
ORIGINAL_ENV_FILE=".env.original"
TEMP_ENV_FILE=".env.test"

# Function to print section headers
print_header() {
    echo -e "\n${BLUE}=======================================${NC}"
    echo -e "${BLUE}   $1${NC}"
    echo -e "${BLUE}=======================================${NC}\n"
}

# Function to print test results
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS: $2${NC}"
    else
        echo -e "${RED}✗ FAIL: $2${NC}"
        echo -e "${RED}  Error details: $3${NC}"
    fi
}

# Function to preserve original environment state
backup_env() {
    if [ -f ".env" ]; then
        echo "Backing up original .env file to $ORIGINAL_ENV_FILE"
        cp .env "$ORIGINAL_ENV_FILE"
    else
        echo "No .env file found, creating a backup of default settings"
        echo "# Original environment backup" > "$ORIGINAL_ENV_FILE"
    fi
}

# Function to restore original environment
restore_env() {
    if [ -f "$ORIGINAL_ENV_FILE" ]; then
        echo "Restoring original .env file"
        cp "$ORIGINAL_ENV_FILE" .env
        rm "$ORIGINAL_ENV_FILE"
    else
        echo "No backup .env file found"
    fi
}

# Function to wait for container to be in a specific state
wait_for_container_state() {
    container_name=$1
    target_state=$2
    max_attempts=30
    attempt=1
    
    echo "Waiting for $container_name to be $target_state (max $max_attempts attempts)..."
    
    while [ $attempt -le $max_attempts ]; do
        container_state=$(docker inspect --format='{{.State.Status}}' "$container_name" 2>/dev/null)
        
        if [ "$container_state" = "$target_state" ]; then
            echo "Container $container_name is now $target_state"
            return 0
        fi
        
        echo "Attempt $attempt/$max_attempts: Container state is $container_state, waiting for $target_state..."
        sleep 2
        attempt=$((attempt+1))
    done
    
    echo "Timeout waiting for container $container_name to be $target_state"
    return 1
}

# Cleanup function to ensure we reset everything
cleanup() {
    print_header "CLEANUP"
    
    echo "Stopping test containers..."
    docker compose -f "$COMPOSE_FILE" down
    
    restore_env
    
    echo "Restarting containers with original settings..."
    docker compose -f "$COMPOSE_FILE" up -d
    
    echo "Cleanup complete."
}

# Ensure cleanup runs on script exit
trap cleanup EXIT

# Start the script
print_header "CONTAINER HEALTH CHECKS TEST SCRIPT"
echo "This script will test the container health check implementations"
echo "Make sure you have docker-compose installed and permissions to run docker commands"

# Backup environment
backup_env

print_header "STARTING CONTAINERS WITH DEFAULT SETTINGS"
docker compose -f "$COMPOSE_FILE" down
docker compose -f "$COMPOSE_FILE" up -d

# Wait for containers to start
sleep 10

# Test 1.1: Verify Django Health Endpoint Response
print_header "TEST 1.1: DJANGO HEALTH ENDPOINT"
echo "Testing the Django health endpoint at http://localhost:8000/health/"

response=$(curl -s -w "\n%{http_code}" http://localhost:8000/health/)
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')

echo -e "Response code: ${YELLOW}$http_code${NC}"
echo -e "Response body: ${YELLOW}$content${NC}"

if [ "$http_code" -eq 200 ] && [[ "$content" == *"healthy"* ]]; then
    print_result 0 "Django health endpoint returns 200 OK and reports healthy status"
else
    print_result 1 "Django health endpoint test failed" "Expected 200 OK, got $http_code"
fi

# Test 1.2: Simulate Database Connection Failure (Detailed Steps)
print_header "TEST 1.2: DATABASE CONNECTION FAILURE SIMULATION"
echo "This test will simulate a database connection failure by modifying environment variables"

# Step 1: Stop all containers
echo "Step 1: Stopping all containers..."
docker compose -f "$COMPOSE_FILE" down
print_result $? "Stopping containers" "Failed to stop containers"

# Step 2: Create a temporary environment file with incorrect DB settings
echo "Step 2: Creating temporary environment file with incorrect DB settings..."
if [ -f ".env" ]; then
    cat .env | sed 's/DB_HOST=.*/DB_HOST=192.168.1.999/' > "$TEMP_ENV_FILE"
else
    # Create minimal .env file with wrong DB settings
    echo "DB_HOST=192.168.1.999" > "$TEMP_ENV_FILE"
    echo "DB_PORT=5432" >> "$TEMP_ENV_FILE"
    echo "DB_NAME=database" >> "$TEMP_ENV_FILE"
    echo "DB_USER=olivier" >> "$TEMP_ENV_FILE"
    echo "DB_PASSWORD=password" >> "$TEMP_ENV_FILE"
fi
cp "$TEMP_ENV_FILE" .env
print_result $? "Creating test .env file" "Failed to create test .env file"

# Step 3: Start containers with incorrect DB settings
echo "Step 3: Starting containers with incorrect DB settings..."
docker compose -f "$COMPOSE_FILE" up -d
print_result $? "Starting containers with incorrect DB settings" "Failed to start containers"

# Step 4: Wait for the Django container to be running
echo "Step 4: Waiting for the Django container to be running..."
sleep 15

# Step 5: Test the health endpoint
echo "Step 5: Testing the health endpoint with DB connection failure..."
response=$(curl -s -w "\n%{http_code}" http://localhost:8000/health/)
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')

echo -e "Response code: ${YELLOW}$http_code${NC}"
echo -e "Response body: ${YELLOW}$content${NC}"

if [ "$http_code" -eq 500 ] && [[ "$content" == *"unhealthy"* ]] && [[ "$content" == *"database"* ]]; then
    print_result 0 "Database connection failure correctly detected"
else
    if [ -z "$http_code" ]; then
        print_result 1 "Django health endpoint unreachable" "Container may have failed to start due to DB connection issues, which is also expected behavior"
    else
        print_result 1 "Database connection failure test failed" "Expected 500 and unhealthy status, got $http_code"
    fi
fi

# Restore normal operation
echo "Restoring normal operation with correct DB settings..."
docker compose -f "$COMPOSE_FILE" down
if [ -f "$ORIGINAL_ENV_FILE" ]; then
    cp "$ORIGINAL_ENV_FILE" .env
fi
docker compose -f "$COMPOSE_FILE" up -d
sleep 15

# Test 2.1: Verify Nginx Health Endpoint
print_header "TEST 2.1: NGINX HEALTH ENDPOINT"
echo "Testing the Nginx health endpoint at http://localhost:8080/nginx-health"

response=$(curl -s -w "\n%{http_code}" http://localhost:8080/nginx-health)
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')

echo -e "Response code: ${YELLOW}$http_code${NC}"
echo -e "Response body: ${YELLOW}$content${NC}"

if [ "$http_code" -eq 200 ] && [[ "$content" == *"OK"* ]]; then
    print_result 0 "Nginx health endpoint returns 200 OK"
else
    print_result 1 "Nginx health endpoint test failed" "Expected 200 OK with 'OK' content, got $http_code with content: '$content'"
    
    # Additional debugging for Nginx
    echo -e "\n${YELLOW}Performing additional Nginx debugging:${NC}"
    echo "Testing Nginx configuration..."
    docker exec -t "$NGINX_CONTAINER" nginx -t || echo "Nginx config test failed"
    
    echo "Checking if Nginx is listening on port 80..."
    docker exec -t "$NGINX_CONTAINER" netstat -tulpn | grep 80 || echo "Nginx not listening on port 80"
    
    echo "Checking internal Nginx health from inside the container..."
    docker exec -t "$NGINX_CONTAINER" curl -I http://localhost/nginx-health || echo "Cannot reach health endpoint from inside container"
fi

# Test 3.1: Check Container Health Status
print_header "TEST 3.1: CONTAINER HEALTH STATUS"
echo "Checking Docker health status for all containers"

docker_ps_output=$(docker ps --format "{{.Names}}: {{.Status}}")
echo -e "Docker ps output:\n${YELLOW}$docker_ps_output${NC}"

django_status=$(echo "$docker_ps_output" | grep "$DJANGO_CONTAINER")
nginx_status=$(echo "$docker_ps_output" | grep "$NGINX_CONTAINER")

echo -e "\nDjango status: ${YELLOW}$django_status${NC}"
echo -e "Nginx status: ${YELLOW}$nginx_status${NC}"

if [[ "$django_status" == *"(healthy)"* ]]; then
    print_result 0 "Django container reports healthy status"
else
    print_result 1 "Django container health check failed" "Expected (healthy) status, got: $django_status"
fi

if [[ "$nginx_status" == *"(healthy)"* ]]; then
    print_result 0 "Nginx container reports healthy status"
else
    print_result 1 "Nginx container health check failed" "Expected (healthy) status, got: $nginx_status"
fi

# Test 3.2: Inspect Detailed Health Status
print_header "TEST 3.2: DETAILED HEALTH STATUS INSPECTION"
echo "Checking detailed health status via docker inspect"

django_health=$(docker inspect --format "{{.State.Health.Status}}" "$DJANGO_CONTAINER" 2>/dev/null)
nginx_health=$(docker inspect --format "{{.State.Health.Status}}" "$NGINX_CONTAINER" 2>/dev/null)

echo -e "Django health: ${YELLOW}$django_health${NC}"
echo -e "Nginx health: ${YELLOW}$nginx_health${NC}"

if [ "$django_health" = "healthy" ]; then
    print_result 0 "Django container inspect shows healthy"
else
    print_result 1 "Django container inspect failed" "Expected 'healthy', got: $django_health"
fi

if [ "$nginx_health" = "healthy" ]; then
    print_result 0 "Nginx container inspect shows healthy"
else
    print_result 1 "Nginx container inspect failed" "Expected 'healthy', got: $nginx_health"
fi

# Test 3.3: View Health Check Logs
print_header "TEST 3.3: HEALTH CHECK LOGS"
echo "Viewing health check logs via docker inspect"

django_health_logs=$(docker inspect --format "{{range .State.Health.Log}}{{.Output}}{{end}}" "$DJANGO_CONTAINER" 2>/dev/null)
nginx_health_logs=$(docker inspect --format "{{range .State.Health.Log}}{{.Output}}{{end}}" "$NGINX_CONTAINER" 2>/dev/null)

echo -e "Django health logs: ${YELLOW}$django_health_logs${NC}"
echo -e "Nginx health logs: ${YELLOW}$nginx_health_logs${NC}"

if [[ "$django_health_logs" == *"200"* ]] || [[ "$django_health_logs" == *"OK"* ]]; then
    print_result 0 "Django health logs show successful checks"
else
    print_result 1 "Django health logs inspection failed" "Expected success indicators in logs"
fi

if [[ "$nginx_health_logs" == *"200"* ]] || [[ "$nginx_health_logs" == *"OK"* ]]; then
    print_result 0 "Nginx health logs show successful checks"
else
    print_result 1 "Nginx health logs inspection failed" "Expected success indicators in logs"
fi

# Test 4.1: Test Automatic Restart on Failure
print_header "TEST 4.1: AUTOMATIC RESTART ON FAILURE"
echo "This test will kill the Gunicorn process to simulate a failure"

echo "Getting current Docker container state before test..."
initial_state=$(docker ps --format "{{.Names}}: {{.Status}}" | grep "$DJANGO_CONTAINER")
echo -e "Initial state: ${YELLOW}$initial_state${NC}"

echo "Killing Gunicorn process in Django container..."
docker exec "$DJANGO_CONTAINER" pkill gunicorn

echo "Waiting to observe container behavior..."
sleep 5

echo "Getting Docker container state after killing Gunicorn..."
after_kill_state=$(docker ps --format "{{.Names}}: {{.Status}}" | grep "$DJANGO_CONTAINER")
echo -e "State after kill: ${YELLOW}$after_kill_state${NC}"

# Wait for potential restart
echo "Waiting for container to recover..."
sleep 15

echo "Getting final Docker container state after recovery period..."
final_state=$(docker ps --format "{{.Names}}: {{.Status}}" | grep "$DJANGO_CONTAINER")
echo -e "Final state: ${YELLOW}$final_state${NC}"

if [[ "$final_state" == *"Up"* ]]; then
    print_result 0 "Django container restarted successfully after process kill"
else
    print_result 1 "Django container restart test failed" "Container state: $final_state"
fi

# Test 4.2: Test Dependency Chain
print_header "TEST 4.2: DEPENDENCY CHAIN"
echo "This test will verify that Nginx waits for Django to be healthy"

echo "Stopping Django container..."
docker stop "$DJANGO_CONTAINER"
print_result $? "Stopping Django container" "Failed to stop container"

echo "Verifying Django container is stopped..."
wait_for_container_state "$DJANGO_CONTAINER" "exited"

echo "Restarting only Nginx container and checking dependency behavior..."
docker compose -f "$COMPOSE_FILE" up -d nginx
sleep 5

echo "Checking if Django container was also started due to dependency..."
django_running=$(docker ps -q -f name="$DJANGO_CONTAINER")
if [ -n "$django_running" ]; then
    print_result 0 "Django container was automatically started as a dependency"
else
    print_result 1 "Dependency chain test failed" "Django container was not started"
fi

echo "Starting Django container explicitly..."
docker compose -f "$COMPOSE_FILE" up -d django
sleep 15

echo "Final container status after dependency test:"
docker ps --format "{{.Names}}: {{.Status}}" | grep -E "$DJANGO_CONTAINER|$NGINX_CONTAINER"

# Test 5: Summary
print_header "TEST SUMMARY"
echo "All health check tests have been completed."
echo "Each test has provided individual pass/fail results above."
echo "The original environment has been restored."

echo -e "\n${GREEN}Health check testing script completed.${NC}"
echo "You can now inspect the results above to ensure all aspects of the health checks are working."
echo "If any tests failed, review the error details for troubleshooting guidance." 