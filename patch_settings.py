#!/usr/bin/env python3
"""
A script to patch Django settings directly.
"""
import os
import sys

# Path to the settings file
settings_file = 'jarvis/settings.py'

# Debug settings to insert
debug_settings = """
# Debug settings added by patch script
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.129', 'jarvis', 'jarvis.localhost', '*']
CORS_ALLOW_ALL_ORIGINS = True
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny']

# Enhanced logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
"""

# First, check if the file exists
if not os.path.exists(settings_file):
    print(f"Settings file {settings_file} not found!")
    sys.exit(1)

# Read the current contents
with open(settings_file, 'r') as f:
    lines = f.readlines()

# Find where to insert the debug settings
for i, line in enumerate(lines):
    if "DEBUG =" in line:
        # Replace the DEBUG line and add the other settings afterward
        lines[i] = debug_settings
        break

# Write the updated file
with open(settings_file, 'w') as f:
    f.writelines(lines)

print(f"Successfully patched {settings_file} with debug settings.")

# Replace the entire urls.py file
urls_file = 'jarvis/urls.py'

# Complete urls.py content with all necessary test endpoints
urls_content = """
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def super_basic_test(request):
    """An absolute minimal view that just returns a string with no dependencies."""
    return HttpResponse("OK", content_type="text/plain")

def basic_test(request):
    """A basic view that returns a simple HTTP response for debugging."""
    try:
        logger.info(f"Basic test accessed: {request.path}, Method: {request.method}")
        logger.info(f"Request headers: {request.headers}")
        return HttpResponse("Basic test view is working", content_type="text/plain")
    except Exception as e:
        logger.error(f"Error in basic_test: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", content_type="text/plain", status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_test(request):
    """A simple API test endpoint."""
    try:
        logger.info(f"API test accessed: {request.path}, Method: {request.method}")
        return Response({
            'status': 'OK',
            'message': 'API test endpoint is working'
        })
    except Exception as e:
        logger.error(f"Error in api_test: {str(e)}")
        return Response({
            'status': 'ERROR',
            'message': str(e)
        }, status=500)

@api_view(['GET'])
def api_root(request):
    """Root API endpoint."""
    return Response({
        'status': 'OK',
        'message': 'Jarvis API is running'
    })

urlpatterns = [
    # Admin and authentication
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    
    # Test endpoints with multiple paths for testing
    path('', api_root),
    path('super-basic-test/', super_basic_test),
    path('basic-test/', basic_test),
    path('test/', api_test),
    
    # API test endpoints with /api prefix
    path('api/test/', api_test),
    path('api/', api_root),
    
    # API endpoints
    path('api/administrative/', include('administrative.api.urls')),
    path('api/health/', include('health.api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

# Write the complete urls file
with open(urls_file, 'w') as f:
    f.write(urls_content)

print(f"Successfully updated {urls_file} with debug views.")

# Create a test view to check response directly
test_view_path = 'jarvis/test_view.py'
test_view_content = """
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Test view is working!", content_type="text/plain")
"""

with open(test_view_path, 'w') as f:
    f.write(test_view_content)

print(f"Created test view at {test_view_path}.")

# Print instructions for manual verification
print("\nPatch complete. You should now be able to access the following endpoints:")
print("- http://localhost/basic-test/")
print("- http://localhost/super-basic-test/")
print("- http://localhost/api/test/")
print("- http://localhost/api/health/symptoms/")
print("\nIf issues persist, check Docker logs with: docker compose logs backend") 