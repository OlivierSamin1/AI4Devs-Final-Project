#!/usr/bin/env python3
import os
import sys

# Path to the urls file
urls_path = '/app/jarvis/urls.py'

# Check if file exists
if not os.path.exists(urls_path):
    print(f"Error: URLs file not found at {urls_path}")
    sys.exit(1)

# Read the current urls file
with open(urls_path, 'r') as f:
    urls_content = f.read()

# Fix any incomplete import statements
if 'from django.urls import' in urls_content and '\n' in urls_content.split('from django.urls import')[1].split('\n')[0]:
    # The import is incomplete and ends with a newline
    urls_content = urls_content.replace('from django.urls import', 'from django.urls import path, include')

# Create a completely fixed urls.py file
fixed_urls = """from django.contrib import admin
from django.urls import path, include
from jarvis.test_view import test_view
from jarvis.settings import basic_test_view, super_basic_test_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jarvis.api_urls')),
    path('test/', test_view),
    path('basic-test/', basic_test_view),
    path('super-basic-test/', super_basic_test_view),
]
"""

# Write the fixed urls file
with open(urls_path, 'w') as f:
    f.write(fixed_urls)

# Check if api_urls.py exists, create it if it doesn't
api_urls_path = '/app/jarvis/api_urls.py'
if not os.path.exists(api_urls_path):
    api_urls = """from django.urls import path, include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('finances/', include('finances.urls')),
    path('real-estate/', include('real_estate.urls')),
    path('tax/', include('tax.urls')),
    path('transportation/', include('transportation.urls')),
    path('health/', include('health.urls')),
    path('administrative/', include('administrative.urls')),
    path('test/', lambda request: HttpResponse("API test successful!")),
]
"""
    with open(api_urls_path, 'w') as f:
        f.write(api_urls)

print("URLs file fixed successfully!") 