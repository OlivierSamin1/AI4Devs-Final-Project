# Connecting to API from Another Device on Local Network

This guide covers accessing your API running on a Raspberry Pi from another device on the local network.

## Overview

Key points covered:
- Django settings configuration
- Finding your Raspberry Pi's IP address
- Configuring firewall rules
- Testing connections with various tools

## Table of Contents

1. [Django Settings Configuration](#1-django-settings-configuration)
2. [Finding Your Pi's IP Address](#2-finding-your-pis-ip-address)
3. [Verifying API Accessibility](#3-verifying-api-accessibility)
4. [Using Authentication](#4-using-authentication)
5. [Firewall Configuration](#5-firewall-configuration)
6. [Troubleshooting Connection Issues](#6-troubleshooting-connection-issues)

## Implementation Steps

### 1. Django Settings Configuration

Open your Django project's `settings.py` file and update the `ALLOWED_HOSTS` to include your Pi's IP address:

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.X',  # Replace with your Pi's IP address
]
```

For development, you can also enable CORS:

```python
INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this at the top
    # ... other middleware
]

# For development only
CORS_ALLOW_ALL_ORIGINS = True
```

### 2. Finding Your Pi's IP Address

Run this command on your Raspberry Pi:

```bash
hostname -I
```

Note the IP address (typically like `192.168.1.X`).

### 3. Verifying API Accessibility

Start your Django server to listen on all interfaces:

```bash
python manage.py runserver 0.0.0.0:8000
```

Test locally first:

```bash
curl http://localhost:8000/api/your-endpoint/
```

Then test from another device on the network:

```bash
curl http://192.168.1.X:8000/api/your-endpoint/
```

### 4. Using Authentication

If your API uses token authentication, obtain a token:

```bash
curl -X POST http://192.168.1.X:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Then use the token for authenticated requests:

```bash
curl -H "Authorization: Bearer your_access_token" \
  http://192.168.1.X:8000/api/protected-endpoint/
```

### 5. Firewall Configuration

If you're using UFW on your Raspberry Pi, allow traffic on port 8000:

```bash
sudo ufw allow 8000/tcp
```

For better security, restrict to your local network:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 8000 proto tcp
```

Apply the changes:

```bash
sudo ufw reload
```

### 6. Troubleshooting Connection Issues

If you can't connect:

1. Check if the Django server is running and listening on 0.0.0.0
2. Verify firewall rules aren't blocking the connection
3. Ensure both devices are on the same network
4. Check for any CORS issues in browser console
5. Validate the correct IP address is being used

For more detailed diagnostics, check the UFW logs:

```bash
sudo journalctl -u ufw
```

## Next Steps

Now that you can access your API locally, consider setting up secure HTTPS access with Nginx and Let's Encrypt for more secure remote access. 