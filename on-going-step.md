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

### Next Steps
The last change made to the Django application needs to be tested on the Raspberry Pi 4 to confirm whether the 400 Bad Request error persists. This will help determine if the issue is related to the application configuration or if there are other underlying problems that need to be addressed.
