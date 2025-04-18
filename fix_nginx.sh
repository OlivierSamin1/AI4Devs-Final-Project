#!/bin/bash

# Create the nginx configuration file
cat > nginx.conf << 'EOF'
server {
    listen 80;
    server_name jarvis.localhost;
    
    # Direct routes to specific endpoints for testing
    location = /direct-test/ {
        proxy_pass http://backend:8000/direct-test/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Route requests to Django - Put this before the frontend location
    location ~ ^/(api|admin|api-auth|basic-test|super-basic-test|direct-test|test)/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Serve static frontend files for all other requests
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }
}
EOF

# Copy the configuration to the container
docker compose cp nginx.conf nginx:/etc/nginx/conf.d/default.conf

# Restart nginx
docker compose restart nginx

echo "NGINX configuration updated and service restarted" 