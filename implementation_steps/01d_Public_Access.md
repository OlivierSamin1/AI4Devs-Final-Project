# Public Access Configuration

This document outlines the steps to make the web application accessible from the internet, including domain name setup, SSL certificate configuration, and security measures.

## Prerequisites

Ensure you have completed the [Web Application Server Implementation](./01c_Web_Application.md) and the application is running locally before proceeding. Remember that the Raspberry Pi 3B database server is already set up and contains the February 2025 reservation data.

## Domain Name Setup

To access your application from the internet, you'll need a domain name. You can purchase one from a domain registrar like Namecheap, GoDaddy, or Google Domains.

### Option 1: Purchase a Custom Domain

1. Purchase a domain name from a registrar of your choice.
2. Set up DNS records to point to your home IP address.

### Option 2: Use a Free Dynamic DNS Service

1. Sign up for a free dynamic DNS service like:
   - No-IP (https://www.noip.com/)
   - DuckDNS (https://www.duckdns.org/)
   - FreeDNS (https://freedns.afraid.org/)

2. We'll use DuckDNS for this guide:
   - Go to https://www.duckdns.org/ and sign in (using GitHub, Google, etc.)
   - Add a subdomain (e.g., `personal-db-assistant.duckdns.org`)
   - Note your token for future use

3. Install the DuckDNS update client on the Raspberry Pi 4:
   ```bash
   mkdir -p ~/duckdns
   cd ~/duckdns
   ```

4. Create an update script:
   ```bash
   nano duck.sh
   ```

5. Add the following content (replace the token and domain with your own):
   ```bash
   #!/bin/bash
   echo url="https://www.duckdns.org/update?domains=YOUR_SUBDOMAIN&token=YOUR_TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -
   ```

6. Make the script executable:
   ```bash
   chmod 700 duck.sh
   ```

7. Run the script to test it:
   ```bash
   ./duck.sh
   ```

8. Check the log file to ensure it worked:
   ```bash
   cat duck.log
   ```
   You should see "OK" in the log file.

9. Set up a cron job to update the IP address regularly:
   ```bash
   crontab -e
   ```

10. Add the following line to update every 5 minutes:
    ```
    */5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
    ```

## Port Forwarding Configuration

To make your application accessible from the internet, you need to configure port forwarding on your router:

1. Access your router's admin interface (usually by navigating to 192.168.1.1 or similar in a web browser).

2. Find the port forwarding or virtual server settings (varies by router model).

3. Set up port forwarding rules:
   - Forward external port 80 (HTTP) to 192.168.1.10:80 (Raspberry Pi 4)
   - Forward external port 443 (HTTPS) to 192.168.1.10:443 (Raspberry Pi 4)

4. Save your settings and test the connection by visiting your domain in a web browser from a device outside your network (e.g., using mobile data).

5. Note: Do not forward any ports to the Raspberry Pi 3B database server. It should remain inaccessible from the internet for security.

## SSL Certificate Configuration with Let's Encrypt

To secure your application with HTTPS, you'll use Let's Encrypt to get a free SSL certificate:

1. Stop your existing Docker containers:
   ```bash
   cd ~/personal-db-assistant
   docker-compose down
   ```

2. Install Certbot:
   ```bash
   sudo apt-get update
   sudo apt-get install -y certbot
   ```

3. Obtain a certificate using the standalone plugin (ensure your domain is pointing to your IP and port 80 is open):
   ```bash
   sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com
   ```
   Replace `your-domain.com` with your actual domain name. If you're using DuckDNS, it would be something like `your-subdomain.duckdns.org`.

4. The certificates will be stored in `/etc/letsencrypt/live/your-domain.com/`.

5. Create a directory for certificates in your project:
   ```bash
   mkdir -p ~/personal-db-assistant/nginx/certs
   ```

6. Create a script to copy and update certificates:
   ```bash
   nano ~/personal-db-assistant/nginx/update-certs.sh
   ```

7. Add the following content:
   ```bash
   #!/bin/bash
   DOMAIN="your-domain.com"  # Replace with your domain
   
   # Create temporary directory
   mkdir -p ~/personal-db-assistant/nginx/certs
   
   # Copy certificates
   sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem ~/personal-db-assistant/nginx/certs/
   sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ~/personal-db-assistant/nginx/certs/
   
   # Set permissions
   sudo chown $USER:$USER ~/personal-db-assistant/nginx/certs/*
   sudo chmod 644 ~/personal-db-assistant/nginx/certs/*
   
   # Restart Docker containers
   cd ~/personal-db-assistant
   docker-compose restart nginx
   ```

8. Make the script executable:
   ```bash
   chmod +x ~/personal-db-assistant/nginx/update-certs.sh
   ```

9. Run the script to copy the certificates:
   ```bash
   ~/personal-db-assistant/nginx/update-certs.sh
   ```

10. Set up auto-renewal for the certificates:
    ```bash
    sudo crontab -e
    ```

11. Add the following lines to attempt renewal twice daily and update Docker if certificates change:
    ```
    0 */12 * * * certbot renew --quiet --post-hook "/home/pi/personal-db-assistant/nginx/update-certs.sh"
    ```

12. Update your Nginx configuration to use SSL:
    ```bash
    nano ~/personal-db-assistant/nginx/default.conf
    ```

13. Replace the content with:
    ```nginx
    # Main proxy configuration
    server {
        listen 80;
        server_name your-domain.com www.your-domain.com;
        
        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name your-domain.com www.your-domain.com;
        
        ssl_certificate /etc/nginx/certs/fullchain.pem;
        ssl_certificate_key /etc/nginx/certs/privkey.pem;
        
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:10m;
        
        # Serve static files directly from the backend
        location /static/ {
            proxy_pass http://backend:8000/static/;
        }

        # Pass API requests to the backend
        location /api/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Route all other requests to the frontend
        location / {
            proxy_pass http://frontend:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```
    Remember to replace `your-domain.com` with your actual domain.

14. Update the Dockerfile for Nginx to include the SSL certificates:
    ```bash
    nano ~/personal-db-assistant/nginx/Dockerfile
    ```

15. Update the content:
    ```dockerfile
    FROM nginx:alpine

    COPY ./default.conf /etc/nginx/conf.d/default.conf
    COPY ./certs/ /etc/nginx/certs/
    ```

16. Update the docker-compose.yml file:
    ```bash
    nano ~/personal-db-assistant/docker-compose.yml
    ```

17. Update the content:
    ```yaml
    version: '3'

    services:
      # Backend API service
      backend:
        build: ./backend
        restart: always
        volumes:
          - static_volume:/app/staticfiles
          - backend_data:/app/data
        env_file:
          - ./backend/.env
        depends_on:
          - redis
        expose:
          - 8000
        networks:
          - app_network

      # Frontend service
      frontend:
        build: ./frontend
        restart: always
        depends_on:
          - backend
        expose:
          - 80
        networks:
          - app_network
      
      # Redis service for caching
      redis:
        image: redis:alpine
        restart: always
        command: redis-server /usr/local/etc/redis/redis.conf
        volumes:
          - ./redis/redis.conf:/usr/local/etc/redis/redis.conf
          - redis_data:/data
        expose:
          - 6379
        networks:
          - app_network

      # Main web server
      nginx:
        build: ./nginx
        restart: always
        volumes:
          - static_volume:/app/staticfiles
          - ./nginx/certs:/etc/nginx/certs
        ports:
          - "80:80"
          - "443:443"
        depends_on:
          - backend
          - frontend
        networks:
          - app_network

    volumes:
      static_volume:
      backend_data:
      redis_data:
    
    networks:
      app_network:
        driver: bridge
    ```

18. Rebuild and restart the Docker containers:
    ```bash
    cd ~/personal-db-assistant
    docker-compose up -d --build
    ```

## Security Enhancements

### 1. Basic Authentication for Initial Protection

While this is a simple "Hello World" POC, it's good to add basic authentication as a minimal security measure:

1. Install htpasswd utility:
   ```bash
   sudo apt-get install -y apache2-utils
   ```

2. Create a password file:
   ```bash
   mkdir -p ~/personal-db-assistant/nginx/auth
   htpasswd -c ~/personal-db-assistant/nginx/auth/.htpasswd admin
   ```
   Follow the prompts to set a password.

3. Update the Nginx configuration:
   ```bash
   nano ~/personal-db-assistant/nginx/default.conf
   ```

4. Add basic authentication to the SSL server block:
   ```nginx
   server {
       listen 443 ssl;
       # ... existing SSL settings ...
       
       auth_basic "Restricted";
       auth_basic_user_file /etc/nginx/auth/.htpasswd;
       
       # ... existing locations ...
   }
   ```

5. Update the Nginx Dockerfile:
   ```bash
   nano ~/personal-db-assistant/nginx/Dockerfile
   ```

6. Add the auth directory:
   ```dockerfile
   FROM nginx:alpine

   COPY ./default.conf /etc/nginx/conf.d/default.conf
   COPY ./certs/ /etc/nginx/certs/
   COPY ./auth/ /etc/nginx/auth/
   ```

7. Update the docker-compose.yml file to include the auth volume:
   ```bash
   nano ~/personal-db-assistant/docker-compose.yml
   ```

8. Add the auth volume:
   ```yaml
   services:
     nginx:
       # ... existing settings ...
       volumes:
         - static_volume:/app/staticfiles
         - ./nginx/certs:/etc/nginx/certs
         - ./nginx/auth:/etc/nginx/auth
   ```

9. Rebuild and restart the Docker containers:
   ```bash
   cd ~/personal-db-assistant
   docker-compose up -d --build
   ```

### 2. Configure Security Headers

Add security headers to the Nginx configuration:

1. Edit the Nginx configuration:
   ```bash
   nano ~/personal-db-assistant/nginx/default.conf
   ```

2. Add security headers to the SSL server block:
   ```nginx
   server {
       listen 443 ssl;
       # ... existing SSL settings ...
       
       # Security headers
       add_header X-Content-Type-Options "nosniff" always;
       add_header X-Frame-Options "SAMEORIGIN" always;
       add_header X-XSS-Protection "1; mode=block" always;
       add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data:; font-src 'self';" always;
       add_header Referrer-Policy "strict-origin-when-cross-origin" always;
       
       # ... existing locations ...
   }
   ```

3. Rebuild and restart Nginx:
   ```bash
   cd ~/personal-db-assistant
   docker-compose up -d --build nginx
   ```

### 3. Install Fail2Ban for Brute Force Protection

Fail2Ban can help protect your server from brute force attacks:

1. Install Fail2Ban:
   ```bash
   sudo apt-get install -y fail2ban
   ```

2. Create a custom jail for Nginx:
   ```bash
   sudo nano /etc/fail2ban/jail.d/nginx-http-auth.conf
   ```

3. Add the following content:
   ```
   [nginx-http-auth]
   enabled = true
   filter = nginx-http-auth
   port = http,https
   logpath = /var/log/nginx/error.log
   maxretry = 5
   findtime = 300
   bantime = 3600
   ```

4. Start and enable Fail2Ban:
   ```bash
   sudo systemctl start fail2ban
   sudo systemctl enable fail2ban
   ```

## Testing Public Access

1. Test your application by visiting your domain name using HTTPS:
   ```
   https://your-domain.com
   ```

2. Verify that:
   - The HTTPS connection is secure (look for the lock icon in the browser)
   - You're prompted for basic authentication credentials
   - After logging in, you can see the React frontend displaying the FuerteVentura reservations for February 2025
   - The data is being properly fetched from the backend API, which in turn is retrieving it from the existing database on the Raspberry Pi 3B
   - All containerized services (frontend, backend, Redis, Nginx) are working together correctly

3. Check SSL configuration using SSL Labs:
   - Visit https://www.ssllabs.com/ssltest/
   - Enter your domain name and click "Submit"
   - Wait for the test to complete
   - Aim for at least an "A" rating

## Monitoring Access

1. View Nginx access logs:
   ```bash
   docker-compose logs nginx
   ```

2. Monitor fail2ban status:
   ```bash
   sudo fail2ban-client status nginx-http-auth
   ```

3. Check system performance:
   ```bash
   top
   ```

## Conclusion

You have now successfully set up a publicly accessible web application that:
- Has a proper domain name
- Is secured with HTTPS using Let's Encrypt
- Is protected with basic authentication
- Displays reservation data from the existing database server (Raspberry Pi 3B)

This completes the "Hello World" proof of concept. The next steps would be to enhance security measures and develop more sophisticated features as outlined in the project specification.

## Implementation Status

Below is a status table showing the progress of each step in the public access configuration:

| Section | Step | Status | Comments |
|---------|------|--------|----------|
| **Public Access Configuration** | Domain Name Setup | ❌ | Domain name not yet purchased or configured |
| | Port Forwarding Configuration | ❌ | Port forwarding not yet set up on the router |
| | SSL Certificate Configuration | ❌ | SSL certificate not yet obtained from Let's Encrypt |
| | Basic Authentication | ❌ | Basic authentication not yet implemented |
| | Security Headers | ❌ | Security headers not yet configured in Nginx |
| | Fail2Ban Installation | ❌ | Fail2Ban not yet installed for brute force protection |
| | Testing Public Access | ❌ | Public access testing not yet performed |
| | Monitoring Access | ❌ | Access monitoring not yet set up | 