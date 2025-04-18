#!/usr/bin/env python3
import os
import sys

# Path to the api_urls file
api_urls_path = '/app/jarvis/api_urls.py'

# Create the api_urls.py file
api_urls_content = """from django.urls import path, include
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

# Write the api_urls file
with open(api_urls_path, 'w') as f:
    f.write(api_urls_content)

print("API URLs file created successfully!") 