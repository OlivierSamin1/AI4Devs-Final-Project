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
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.129', 'jarvis', 'jarvis.localhost']
CORS_ALLOW_ALL_ORIGINS = True
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny']
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

# Create a simplified urls.py file
urls_file = 'jarvis/urls.py'

# Simple urls.py content
urls_content = """
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from django.http import HttpResponse

def debug_view(request):
    \"\"\"An extremely simple view for debugging.\"\"\"
    return HttpResponse("Hello from Django!", content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Debug endpoint
    path('debug/', debug_view),
    
    # API endpoints
    path('api/administrative/', include('administrative.api.urls')),
    path('api/health/', include('health.api.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

# Write the simplified urls file
with open(urls_file, 'w') as f:
    f.write(urls_content)

print(f"Successfully updated {urls_file} with debug views.") 