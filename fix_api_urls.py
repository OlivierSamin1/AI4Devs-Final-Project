#!/usr/bin/env python3
import os
import sys

# Path to the api_urls file
api_urls_path = '/app/jarvis/api_urls.py'

# Check if file exists
if not os.path.exists(api_urls_path):
    print(f"Error: API URLs file not found at {api_urls_path}")
    sys.exit(1)

# Create a fixed api_urls.py file
fixed_api_urls = """from django.urls import path, include
from django.http import HttpResponse

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

# Write the fixed api_urls file
with open(api_urls_path, 'w') as f:
    f.write(fixed_api_urls)

print("API URLs file fixed successfully!") 