#!/usr/bin/env python3
import os
import sys

# Path to the settings file
settings_path = '/app/jarvis/settings.py'

# Check if file exists
if not os.path.exists(settings_path):
    print(f"Error: Settings file not found at {settings_path}")
    sys.exit(1)

# Read the current settings file
with open(settings_path, 'r') as f:
    settings_content = f.read()

# Fix the settings file
if 'REST_FRAMEWORK' not in settings_content:
    # Define REST_FRAMEWORK if it doesn't exist
    rest_framework_config = """
# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
"""
    
    # Find a good position to insert the REST_FRAMEWORK config (before MIDDLEWARE)
    if 'MIDDLEWARE' in settings_content:
        settings_content = settings_content.replace('MIDDLEWARE = [', f"{rest_framework_config}\nMIDDLEWARE = [")
    else:
        # If MIDDLEWARE not found, append to the end
        settings_content += rest_framework_config

# Make sure ALLOWED_HOSTS includes everything
if "ALLOWED_HOSTS" in settings_content:
    if "'*'" not in settings_content and '"*"' not in settings_content:
        settings_content = settings_content.replace("ALLOWED_HOSTS = [", "ALLOWED_HOSTS = ['*', ")

# Enable debug mode
settings_content = settings_content.replace("DEBUG = False", "DEBUG = True")

# Add basic test view
test_view_code = """
# Simple test view for debugging
from django.http import HttpResponse

def basic_test_view(request):
    return HttpResponse("Basic test successful!")

def super_basic_test_view(request):
    return HttpResponse("Super basic test successful!")
"""

if test_view_code not in settings_content:
    settings_content += test_view_code

# Write back the updated settings
with open(settings_path, 'w') as f:
    f.write(settings_content)

# Update urls.py to include the test views
urls_path = '/app/jarvis/urls.py'
if os.path.exists(urls_path):
    with open(urls_path, 'r') as f:
        urls_content = f.read()
    
    # Import the test views if not already imported
    if 'basic_test_view' not in urls_content:
        if 'from django.urls import' in urls_content:
            urls_content = urls_content.replace('from django.urls import', 'from django.urls import path, include, ')
        else:
            urls_content = 'from django.urls import path, include\n' + urls_content
        
        if 'from jarvis.settings import basic_test_view' not in urls_content:
            urls_content = urls_content.replace('from django.urls import', 'from django.urls import\nfrom jarvis.settings import basic_test_view, super_basic_test_view')
    
    # Add the test URL patterns if not present
    if "'basic-test/'" not in urls_content and '"basic-test/"' not in urls_content:
        if 'urlpatterns = [' in urls_content:
            urls_content = urls_content.replace('urlpatterns = [', 'urlpatterns = [\n    path("basic-test/", basic_test_view),\n    path("super-basic-test/", super_basic_test_view),')
    
    with open(urls_path, 'w') as f:
        f.write(urls_content)

print("Settings successfully updated!") 