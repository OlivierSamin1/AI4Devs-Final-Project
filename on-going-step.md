01c_Web_application.md --> "building and running the app" section

# Ongoing Steps

## Current Issue
We are experiencing a persistent 400 Bad Request error when attempting to access the API endpoints of the Django application running on the Raspberry Pi 4. This issue has been observed both through direct API calls using `curl` and through the frontend application.

### Steps Taken to Diagnose and Fix the Issue

1. **Initial Configuration Check**:
   - Verified that all Docker containers (backend, frontend, and NGINX) are running properly using `docker-compose ps`.
   - Confirmed that the backend service is listening on port 8000 and the NGINX service is correctly configured to forward requests to the backend.

2. **NGINX Configuration**:
   - Updated the NGINX configuration to ensure that API requests are properly proxied to the backend service.
   - Simplified the proxy configuration to handle all requests under the `/api/` path.

3. **Django Settings**:
   - Enabled DEBUG mode in the Django settings to provide more detailed error messages.
   - Configured logging to capture incoming requests and any errors that occur within the API views.

4. **Testing API Endpoints**:
   - Created a simple test endpoint (`/api/test/`) to verify that the API routing is functioning correctly.
   - Attempted to access the test endpoint both through the NGINX proxy and directly from the backend container.

5. **Middleware Adjustments**:
   - Temporarily commented out the CSRF middleware to determine if it was causing the 400 error.
   - Allowed anonymous access to the symptom viewset to facilitate testing.

6. **Direct Backend Access**:
   - Tested direct access to the backend API from within the NGINX container using `curl` to ensure that the backend service is responding correctly.

7. **Basic Test Endpoint**:
   - Added a basic test view to the Django application to confirm that the application is capable of returning a simple HTTP response.

8. **Applied Configuration Patch**:
   - Created a patch script (`patch_settings.py`) to directly modify the Django settings inside the container.
   - The script sets `DEBUG=True`, adds all necessary hosts to `ALLOWED_HOSTS`, enables CORS for all origins, and sets the default permission class to `AllowAny`.
   - The script also updated the URLs configuration to include simplified debug views.
   - Successfully copied the patch script to the container with `docker compose cp patch_settings.py backend:/app/`.
   - Successfully executed the patch script inside the container with `docker compose exec backend python /app/patch_settings.py`.

### Next Steps
Now that we've applied the patch to simplify the Django configuration and enable debugging, we need to verify if this resolves the 400 Bad Request issue:

1. **Test the basic endpoints** to verify basic functionality:
   ```bash
   curl http://jarvis.localhost/basic-test/
   curl http://jarvis.localhost/debug/
   ```

2. **Test the API endpoints** with and without authentication:
   ```bash
   curl http://jarvis.localhost/api/test/
   curl http://jarvis.localhost/api/health/symptoms/
   curl -H "Authorization: Token 11d3acee94a184b88afa091ed3df7ef71850bffd" http://jarvis.localhost/api/health/symptoms/
   ```

3. **Check container logs** if issues persist:
   ```bash
   docker compose logs backend
   ```

4. **Review NGINX logs** for any proxy-related issues:
   ```bash
   docker compose logs nginx
   ```

5. **Restart containers** if necessary to ensure all changes take effect:
   ```bash
   docker compose restart backend nginx
   ```

After running these tests, we should have a clearer picture of whether the issue has been resolved or if further debugging is required. If the 400 error persists, we'll need to analyze the logs to identify any specific error messages or patterns.