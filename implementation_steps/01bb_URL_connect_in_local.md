# Connecting to your Django REST Framework API on Raspberry Pi from Another PC on Local Network

## Overview

This guide will walk you through the steps needed to access your Django REST Framework API running on your Raspberry Pi from another PC on your local network using a URL.

## Prerequisites

- Raspberry Pi 4 running your Django REST Framework API
- Working token-based authentication
- Another PC on the same local network
- Both devices connected to the same router/network

## Step 1: Configure Django Settings

1. Open your Django project's settings file (`settings.py`) on the Raspberry Pi and add your Raspberry Pi's local IP address to the `ALLOWED_HOSTS` list:

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.129',  # Your Raspberry Pi's IP address
    '*',  # Optional: Allow all hosts (only for development)
]
```

2. If using CORS (for browser-based requests), make sure to configure CORS correctly:

```python
INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # This should be at the top
    # ... other middleware
]

# For development only - restrict this in production
CORS_ALLOW_ALL_ORIGINS = True  

# Or specify allowed origins
# CORS_ALLOWED_ORIGINS = [
#     "http://192.168.1.Y",  # The IP of your other PC
# ]
```

## Step 2: Find Your Raspberry Pi's IP Address

1. On your Raspberry Pi, open a terminal and run:

```bash
hostname -I
```

2. Note the IP address (in this case, it's `192.168.1.129`).

## Step 3: Make Sure Your API is Running and Accessible

1. Start your Django server to listen on all interfaces (not just localhost):

```bash
python manage.py runserver 0.0.0.0:8000
```

2. Test access from the Raspberry Pi itself:

```bash
curl http://localhost:8000/api/health/symptoms/
```

## Step 4: Accessing from Another PC

### Using a Web Browser

1. On your other PC, open a web browser and navigate to:

```
http://192.168.1.129:8000/api/health/symptoms/
```

Replace:
- `8000` with the port your Django server is running on if different

### Using cURL with Real Examples

#### 1. Obtaining an Authentication Token

To get your authentication token, you need to send a POST request to the token endpoint with your credentials:

```bash
curl -X POST http://192.168.1.129:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

This will return a response like:

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

#### 2. Accessing the Health Symptoms API (List All Symptoms)

Now, use the token to retrieve the list of symptoms:

```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  http://192.168.1.129:8000/api/health/symptoms/
```

The response will look something like:

```json
[
  {
    "id": 1,
    "url": "http://192.168.1.129:8000/api/health/symptoms/1/",
    "name": "Headache",
    "child": true,
    "adult": true,
    "products": [1, 2],
    "comments": {"severity": "mild to severe", "duration": "varies"}
  },
  {
    "id": 2,
    "url": "http://192.168.1.129:8000/api/health/symptoms/2/",
    "name": "Fever",
    "child": true,
    "adult": true,
    "products": [3],
    "comments": {"temperature_range": "38-40°C"}
  }
]
```

#### 3. Retrieving a Specific Symptom

To get details about a specific symptom (with ID=1):

```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  http://192.168.1.129:8000/api/health/symptoms/1/
```

#### 4. Fetching Products Associated with a Symptom

To get products recommended for a specific symptom (with ID=1):

```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  http://192.168.1.129:8000/api/health/symptoms/1/products/
```

#### 5. Filtering Symptoms

You can filter symptoms by various criteria:

```bash
# Filter symptoms applicable to children
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  "http://192.168.1.129:8000/api/health/symptoms/?child=true"

# Search for symptoms by name
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  "http://192.168.1.129:8000/api/health/symptoms/?name=head"
```

### Using a REST Client (like Postman)

1. Create a new request in Postman
2. Enter URL: `http://192.168.1.129:8000/api/health/symptoms/`
3. For authenticated requests:
   - Go to the "Authorization" tab
   - Select "API Key" or "Bearer Token" from the Type dropdown (depending on your setup)
   - For API Key: Enter "Authorization" as the Key and "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" as the Value
   - For Bearer Token: Enter your token in the "Token" field
4. Click "Send" to make the request

## Step 5: Configuring Security

For a more secure setup, consider implementing:

1. Use HTTPS with a self-signed certificate or Let's Encrypt
2. Restrict CORS to specific origins
3. Configure a proper firewall on your Raspberry Pi
4. Set up rate limiting for API requests

## Troubleshooting

### Connection Refused

- Ensure Django is running and listening on all interfaces (`0.0.0.0`)
- Check if any firewall is blocking the port (ufw, iptables)

### CORS Issues (for browser requests)

- Verify CORS headers are properly configured
- Check browser console for CORS-related errors

### Authentication Problems

- Ensure token format is correct (including the "Token " prefix)
- Check token expiration
- Verify credentials when requesting a new token

## UFW Firewall Configuration

If you're encountering a "Connection refused" error, it could be because the UFW (Uncomplicated Firewall) is blocking the connection to your Django server. Here's how to check and configure your UFW firewall:

### 1. Check UFW Status

First, check if UFW is active and what rules are currently in place:

```bash
sudo ufw status verbose
```

This will show you if the firewall is active and list all the rules. Look for any rules that might be blocking port 8000.

### 2. Check if UFW is Enabled

If you don't see any output from the previous command, check if UFW is installed:

```bash
sudo apt-get install ufw
```

### 3. Allow Traffic on Port 8000

If UFW is active and no rule allows traffic on port 8000, add a rule to allow it:

```bash
sudo ufw allow 8000/tcp
```

This command allows TCP traffic on port 8000 from any IP address.

### 4. Restrict Access to Your Local Network Only (Optional but Recommended)

For better security, you can restrict access to only your local network:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 8000 proto tcp
```

Replace `192.168.1.0/24` with your actual local network subnet if different.

### 5. Apply the Changes

After adding the rules, apply the changes:

```bash
sudo ufw reload
```

### 6. Verify the Rules

Check that your new rules have been added correctly:

```bash
sudo ufw status numbered
```

### 7. Test Connection After UFW Changes

After making changes to UFW, test the connection again:

```bash
# From Raspberry Pi
curl http://localhost:8000/api/health/symptoms/

# From another PC on the network
curl http://192.168.1.129:8000/api/health/symptoms/
```

### 8. Check Port Binding

Make sure Django is actually listening on all interfaces. You can verify this with:

```bash
sudo ss -tulpn | grep 8000
```

You should see something like:
```
tcp   LISTEN 0  128  0.0.0.0:8000  0.0.0.0:*  users:(("python",pid=12345,fd=3))
```

The `0.0.0.0:8000` indicates it's listening on all interfaces.

### 9. Check Logs for More Information

If you're still having issues, check the system logs for more information:

```bash
sudo journalctl -u ufw
```

### 10. Temporarily Disable UFW for Testing

If you want to verify that UFW is indeed the issue, you can temporarily disable it (be careful in production environments):

```bash
sudo ufw disable
```

Then test your connection. If it works with UFW disabled, you know the firewall was blocking your connection.

Remember to re-enable it after testing:

```bash
sudo ufw enable
```

## Next Steps

- Configure a domain name with your router for easier access
- Set up Nginx as a reverse proxy for better performance and security
- Implement HTTPS for secure communication 